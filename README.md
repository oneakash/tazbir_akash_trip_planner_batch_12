# Smart Group Trip Planner API

A REST API application built with **Python, Flask, and SQLite** for managing group trips, travelers, expenses, and trip lifecycle rules.

This project is developed for the **Internship Batch 12 - Smart Group Trip Planner API Challenge**.

The main focus of this project is implementing correct business logic, persistent data storage, API design, validation, and reproducible setup.

---

## Features

The API supports:

- Trip creation and management
- Traveler management
- Expense tracking
- Trip summary calculation
- Trip status lifecycle management
- Business rule validation
- SQLite persistence

---

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| Framework | Flask |
| Database | SQLite |
| Validation | Pydantic |
| API Format | JSON |

---

# Project Structure

```
trip_planner/

├── run.py
├── run.sh
├── requirements.txt
├── README.md
├── .gitignore
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   ├── services.py
│   ├── schemas.py
│   └── exceptions.py
│
└── instance/
    └── trip_planner.db
```

---

# Prerequisites

Required:

- Python 3
- pip
- Git

For Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
```

---

# Running the Application

## Recommended Method (Fresh Clone)

Clone the repository:

```bash
git clone <repository-url>

cd trip_planner
```

Run:

```bash
./run.sh
```

The script automatically:

- Creates or reuses `.venv`
- Installs dependencies from `requirements.txt`
- Initializes SQLite database tables
- Starts the Flask API

The API will run at:

```
http://127.0.0.1:5000
```

---

# Manual Run Instructions

Create virtual environment:

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start application:

```bash
python run.py
```

---

# API Endpoints

## Health Check

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API availability |

---

## Trip APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/trips` | Create trip |
| GET | `/api/v1/trips` | List all trips |
| GET | `/api/v1/trips/<trip_id>` | Get single trip |
| PUT | `/api/v1/trips/<trip_id>` | Update trip |
| DELETE | `/api/v1/trips/<trip_id>` | Delete trip |

---

## Traveler APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/trips/<trip_id>/travelers` | Add traveler |
| DELETE | `/api/v1/trips/<trip_id>/travelers/<traveler_id>` | Remove traveler |

---

## Expense APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/trips/<trip_id>/expenses` | Add expense |

---

## Status and Summary APIs

| Method | Endpoint | Description |
|---|---|---|
| PATCH | `/api/v1/trips/<trip_id>/status` | Change trip status |
| GET | `/api/v1/trips/<trip_id>/summary` | Get trip summary |

---

# Example Requests

## Health Check

Request:

```bash
curl http://127.0.0.1:5000/health
```

Response:

```json
{
    "status":"ok"
}
```

---

# Create Trip

Request:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips \
-H "Content-Type: application/json" \
-d '{
    "destination":"Coxs Bazar",
    "start_date":"2026-12-01",
    "end_date":"2026-12-05",
    "budget":50000,
    "max_travelers":5
}'
```

Response:

```json
{
    "id":1,
    "message":"Trip created successfully"
}
```

---

# Add Traveler

Request:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips/1/travelers \
-H "Content-Type: application/json" \
-d '{
    "name":"Ayesha Rahman",
    "email":"ayesha@example.com"
}'
```

Response:

```json
{
    "id":1,
    "message":"Traveler added successfully"
}
```

---

# Add Expense

Request:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips/1/expenses \
-H "Content-Type: application/json" \
-d '{
    "title":"Hotel",
    "amount":12000
}'
```

Response:

```json
{
    "id":1,
    "message":"Expense added successfully"
}
```

---

# Trip Summary Example

Request:

```bash
curl http://127.0.0.1:5000/api/v1/trips/1/summary
```

Response:

```json
{
    "traveler_count":1,
    "available_seats":4,
    "total_expense":12000,
    "remaining_budget":38000
}
```

---

# Business Rules

## Trip Rules

- Destination cannot be empty.
- `end_date` must be later than `start_date`.
- Budget must be greater than zero.
- Maximum travelers must be greater than zero.

---

## Traveler Rules

- Same traveler cannot join the same trip twice.
- Email is used as traveler identity.
- Trip capacity cannot be exceeded.
- Traveler cannot join overlapping trips.

---

## Expense Rules

- Expense amount must be greater than zero.
- Total expenses cannot exceed trip budget.
- Spending exactly the remaining budget is allowed.

---

## Lifecycle Rules

Allowed transitions:

```
PLANNED → ONGOING
PLANNED → CANCELLED

ONGOING → COMPLETED
ONGOING → CANCELLED
```

Invalid transitions are rejected.

Examples:

```
PLANNED → COMPLETED ❌

ONGOING → PLANNED ❌

COMPLETED → ONGOING ❌
```

---

# Status Restrictions

| Operation | Allowed Status |
|---|---|
| Add traveler | PLANNED |
| Add expense | PLANNED, ONGOING |
| Edit trip | PLANNED, ONGOING |
| Completed trip modification | Not allowed |
| Cancelled trip modification | Not allowed |

---

# HTTP Response Codes

| Code | Meaning |
|---|---|
| 200 | Successful retrieval/update/delete |
| 201 | Resource created |
| 400 | Validation error |
| 404 | Resource not found |
| 409 | Business rule conflict |

---

# SQLite Database

The application uses SQLite for persistent storage.

Database location:

```
instance/trip_planner.db
```

The database and tables are automatically created during application startup.

No manual SQL execution is required.

The database file is ignored by Git and should not be committed.

---

# Environment Files Ignored

The following files are excluded:

```
.venv/
__pycache__/
*.pyc
*.db
*.sqlite
*.sqlite3
.env
.vscode/
```

---

# Error Response Format

Example:

```json
{
    "error":"TRIP_FULL",
    "message":"The trip has reached its maximum traveler capacity."
}
```

---

# Development Progress

## Completed

- Flask application setup
- SQLite persistence
- Trip CRUD operations
- Traveler management
- Expense management
- Trip summary
- Lifecycle management
- Business validation

---

# Known Limitations

- No frontend interface
- No authentication system
- No deployment configuration

These features are outside the assignment scope.

---

# Running Tests

Basic health check:

```bash
curl -i http://127.0.0.1:5000/health
```

The expected response:

```json
{
    "status":"ok"
}
```
