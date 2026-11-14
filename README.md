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
