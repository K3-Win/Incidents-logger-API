# Incident Logger API

A mini backend project built to practice designing RESTful APIs, role-based token validation, relational constraints, and automated API testing.

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Database:** SQLite (`sqlite3`)
- **Testing:** Pytest, HTTPX (`TestClient`), Postman

## Key Concepts Practiced

- **RESTful API & HTTP Semantics:** Implemented `GET`, `POST`, and `DELETE` endpoints returning accurate status codes (`200`, `201`, `403`, `404`, `409`).
- **Role-Based Access Control (RBAC):** Validated `Authorization: Bearer` headers to separate permissions between `Dev888` (create) and `Checker888` (resolve).
- **Database Integrity:** Enforced a composite primary key `(service, incident)` in SQLite to prevent duplicate active records.
- **Automated Testing:** Tested endpoint behavior manually with Postman (`pm.test`) and automated full-lifecycle integration tests (`POST` -> `GET` -> `DELETE`) using `pytest`.

## Endpoints

| Method | Endpoint | Auth | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | None | Health check |
| `POST` | `/api/incidents` | `Dev888` | Report a new incident (`201` / `409`) |
| `GET` | `/api/incidents` | None | List incidents with optional `?service=` filter (`200`) |
| `DELETE` | `/api/incidents` | `Checker888` | Resolve and delete an incident (`200` / `404`) |

## Quick Start

```bash
# Install dependencies
py -m pip install -r requirements.txt

# Run server
py -m uvicorn main:app --reload

# Run automated tests
py -m pytest test_main.py -v
```
