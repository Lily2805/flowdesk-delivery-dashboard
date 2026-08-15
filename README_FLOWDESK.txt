FLOWDESK DELIVERY DASHBOARD

1. Put these files in the same folder:
   - flowdesk_delivery_dashboard.html
   - server.py
   - flowdesk_seed.json
   - start_flowdesk.bat

2. Start the app:
   - Double-click start_flowdesk.bat
   OR
   - Open Command Prompt in this folder and run: python server.py

3. Open:
   http://localhost:8766/flowdesk_delivery_dashboard.html

4. Backend health:
   http://localhost:8766/api/health

5. Data:
   - flowdesk.db is created automatically.
   - Project changes are persisted to SQLite.
   - The browser keeps a local fallback copy for resilience.
   - The UI shows Backend connected / Local fallback.

6. Reset:
   Use the Reset Demo Data action in the dashboard. It restores the seed dataset in the SQLite database.

IMPORTANT:
- Do not run a second web server on port 8766 at the same time.
- Python 3.10+ recommended.
- No pip packages are required; the backend uses Python's standard library.
- This is a local demo backend, not a production authentication/security stack.
