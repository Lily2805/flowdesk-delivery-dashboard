#!/usr/bin/env python3
import json, sqlite3, threading
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / 'flowdesk.db'
HOST = '0.0.0.0'
PORT = 8766
LOCK = threading.Lock()

SCHEMA = '''
CREATE TABLE IF NOT EXISTS app_state (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  version INTEGER NOT NULL DEFAULT 1,
  data TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
'''

SEED = None

def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def db_conn():
    c = sqlite3.connect(DB_PATH, timeout=10)
    c.execute('PRAGMA journal_mode=WAL')
    c.execute('PRAGMA foreign_keys=ON')
    return c

def init_db(seed):
    with db_conn() as con:
        con.executescript(SCHEMA)
        row = con.execute('SELECT id FROM app_state WHERE id=1').fetchone()
        if not row:
            con.execute('INSERT INTO app_state(id,version,data,updated_at) VALUES(1,1,?,?)',
                         (json.dumps(seed, separators=(',', ':')), now()))

def load_state():
    with db_conn() as con:
        row = con.execute('SELECT version,data,updated_at FROM app_state WHERE id=1').fetchone()
        if not row:
            return {'version': 1, 'updatedAt': now(), 'projects': []}
        return {'version': row[0], 'updatedAt': row[2], **json.loads(row[1])}

def save_state(data, expected_version=None):
    payload = {'projects': data.get('projects', [])}
    with LOCK, db_conn() as con:
        row = con.execute('SELECT version FROM app_state WHERE id=1').fetchone()
        current = row[0] if row else 0
        if expected_version is not None and current != expected_version:
            raise ValueError(f'CONFLICT:{current}')
        newv = current + 1
        updated_at = now()
        con.execute('UPDATE app_state SET version=?, data=?, updated_at=? WHERE id=1',
                    (newv, json.dumps(payload, separators=(',', ':')), updated_at))
        return {'version': newv, 'updatedAt': updated_at, **payload}

class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, '.js':'application/javascript', '.json':'application/json'}

    def log_message(self, fmt, *args):
        print(f'[{self.log_date_time_string()}] {self.address_string()} {fmt%args}')

    def _json(self, code, obj):
        raw = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(raw)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(raw)

    def _body(self):
        n = int(self.headers.get('Content-Length','0'))
        if n > 5_000_000:
            raise ValueError('Payload too large')
        raw = self.rfile.read(n)
        return json.loads(raw.decode('utf-8')) if raw else {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET,POST,PUT,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type, If-Match')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/health':
            self._json(200, {'ok': True, 'service':'flowdesk-api', 'database': str(DB_PATH.name), 'time': now()}); return
        if path == '/api/state':
            self._json(200, load_state()); return
        return super().do_GET()

    def do_PUT(self):
        path = urlparse(self.path).path
        if path != '/api/state':
            self._json(404, {'error':'Not found'}); return
        try:
            data = self._body()
            if not isinstance(data, dict) or not isinstance(data.get('projects'), list):
                raise ValueError('Invalid state payload')
            expected = self.headers.get('If-Match')
            expected = int(expected) if expected else None
            saved = save_state(data, expected)
            self._json(200, saved)
        except ValueError as e:
            msg = str(e)
            if msg.startswith('CONFLICT:'):
                self._json(409, {'error':'State changed on server','version':int(msg.split(':')[1])})
            else:
                self._json(400, {'error':msg})
        except Exception as e:
            self._json(500, {'error':'Server error','detail':str(e)})

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/api/reset':
            try:
                if SEED is None: raise ValueError('Seed unavailable')
                saved = save_state(SEED)
                self._json(200, saved)
            except Exception as e: self._json(500, {'error':str(e)})
            return
        self._json(404, {'error':'Not found'})

    def do_DELETE(self):
        self._json(405, {'error':'Use PUT /api/state for demo state mutations'})

if __name__ == '__main__':
    html = BASE / 'flowdesk_delivery_dashboard.html'
    if not html.exists():
        raise SystemExit('flowdesk_delivery_dashboard.html not found next to server.py')
    # Read the seed directly from a small generated JSON file if present.
    seed_file = BASE / 'flowdesk_seed.json'
    if not seed_file.exists():
        raise SystemExit('flowdesk_seed.json not found. Run the setup generator first.')
    SEED = json.loads(seed_file.read_text(encoding='utf-8'))
    init_db(SEED)
    print(f'FlowDesk running at http://localhost:{PORT}/flowdesk_delivery_dashboard.html')
    print(f'API health: http://localhost:{PORT}/api/health')
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
