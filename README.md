# Incident Logger API

A lightweight RESTful backend service built with FastAPI and SQLite for tracking, querying, and resolving service incidents. Designed with Role-Based Access Control (RBAC) via Bearer tokens, duplicate prevention using composite primary keys, and automated end-to-end lifecycle testing.

## Features

- **Role-Based Access Control (RBAC):** Enforces authorization levels using Bearer tokens (`Dev888` for reporting incidents, `Checker888` for resolving incidents).
- **Duplicate Prevention:** Uses a composite primary key `(service, incident)` in SQLite to prevent duplicate active incident reports (`409 Conflict`).
- **Query Filtering:** Supports filtering reported incidents by service name via query parameters.
- **Automated Testing:** Includes a full-lifecycle integration test suite using `pytest` and FastAPI `TestClient` covering success, conflict, forbidden, and not-found scenarios.

## Tech Stack

- **Framework:** FastAPI, Uvicorn
- **Database:** SQLite (`sqlite3`)
- **Testing:** Pytest, HTTPX (`TestClient`), Postman

## Project Structure

```text
incident-logger-api/
├── main.py              # FastAPI application, RBAC validation, and SQLite operations
├── test_main.py         # Automated end-to-end lifecycle tests using pytest
├── requirements.txt     # Project dependencies
└── .gitignore           # Excludes local SQLite database and cache files
```

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/K3-Win/incident-logger-api.git
   cd incident-logger-api
   ```

2. Install dependencies:
   ```bash
   py -m pip install -r requirements.txt
   ```

### Running the Server

Start the development server with Uvicorn:
```bash
py -m uvicorn main:app --reload
```
The API will be available at `[http://127.0.0.1:8000](http://127.0.0.1:8000)`. Interactive Swagger documentation is accessible at `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`.

## API Reference

### Authentication

Protected endpoints require an `Authorization` header with a Bearer token:
- **Developer Role:** `Authorization: Bearer Dev888`
- **Checker Role:** `Authorization: Bearer Checker888`

### Endpoints

| Method | Endpoint | Auth Required | Description | Success Status |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | None | Health check endpoint | `200 OK` |
| `POST` | `/api/incidents` | `Dev888` | Report a new service incident | `201 Created` |
| `GET` | `/api/incidents` | None | Retrieve incidents (optional `?service=` filter) | `200 OK` |
| `DELETE` | `/api/incidents` | `Checker888` | Resolve and remove an existing incident | `200 OK` |

#### Example Requests

**Report an Incident (`POST /api/incidents`)**
```bash
curl -X POST "http://127.0.0.1:8000/api/incidents" \
  -H "Authorization: Bearer Dev888" \
  -H "Content-Type: application/json" \
  -d '{"service": "payment", "incident": "INC-01"}'
```

**Get Incidents by Service (`GET /api/incidents?service=payment`)**
```bash
curl -X GET "http://127.0.0.1:8000/api/incidents?service=payment"
```

**Resolve an Incident (`DELETE /api/incidents`)**
```bash
curl -X DELETE "http://127.0.0.1:8000/api/incidents" \
  -H "Authorization: Bearer Checker888" \
  -H "Content-Type: application/json" \
  -d '{"service": "payment", "incident": "INC-01"}'
```

## Running Tests

Execute the automated integration test suite (verifies `201`, `409`, `403`, `200`, and `404` state transitions and cleans up test records automatically):

```bash
py -m pytest test_main.py -v
```
