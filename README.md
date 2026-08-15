--- FlowDesk — Project Delivery Intelligence Dashboard

> A full-stack delivery control center that turns scattered project updates into structured, actionable project status.

---Overview---

FlowDesk is a project delivery management platform designed to solve a common problem in customer delivery:

Project updates are often scattered across chats, emails and calls, making it difficult for delivery teams and customers to understand what is happening, what is blocked, and what needs to happen next.

FlowDesk brings projects, milestones, tasks, issues, updates and customer actions into one unified workspace.

---
 Features

---Project Overview---

- Portfolio-wide project visibility
- Project health scores
- Progress tracking
- At Risk / Blocked / On Track states
- Owner visibility
- Upcoming and overdue work

---Project Management---

- Projects
- Milestones
- Tasks
- Multiple project owners
- Task status tracking
- Due dates
- Progress calculation
- Kanban-style workflow

---Issue Management---

Supports the delivery issue taxonomy:

- Bug
- Feature Request
- Question
- Support
- Implementation

Issues can include owners, priority, status, due dates and next actions.

---Activity Intelligence---

FlowDesk converts unstructured delivery updates into structured project information.

Example:

---Unstructured update---

> "Webhook configuration still needs confirmation from the customer before we can start integration testing."

↓

---Structured state---

- Project: SkyFleet
- Status: At Risk
- Blocker: Webhook confirmation
- Impact: Integration testing delayed
- Next Action: Customer confirmation

---Internal + Customer Workspaces---

The same project can have two different experiences.

---Internal workspace---

- Full project state
- Internal risks
- Owners
- Issues
- Activity
- Delivery details

---Customer workspace---

- Customer-safe project progress
- Milestones
- Tasks
- Shared documents
- Customer actions
- Updates relevant to the customer

---FlowDesk Assistant---

A rule-based delivery assistant that can answer questions such as:

- Which projects are blocked?
- Which projects are at risk?
- What is delaying SkyFleet?
- Which customer actions are pending?
- Which projects have stale updates?
- What is the current portfolio health?

The assistant uses the current project state as its source of information.

---Customer Actions---

Delivery blockers can be connected to explicit customer actions.

Example:

```text
Customer must confirm webhook configuration
                    ↓
Integration testing blocked
                    ↓
Customer completes action
                    ↓
Delivery state updated
