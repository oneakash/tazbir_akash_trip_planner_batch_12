# Smart Group Trip Planner API

An individual internship assignment built with Python, Flask, and SQLite.

## Prerequisites

- Python 3 with pip and venv support
- Git
- Bash on Ubuntu/Linux
- Internet access to install dependencies

On Ubuntu, install the required tools if needed:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
```

## Primary Run Command

Clone the repository, enter its directory, and run:

```bash
./run.sh
```

The script creates or reuses `.venv`, installs dependencies from
`requirements.txt`, and starts the API on `127.0.0.1:5000`.

Application startup automatically creates the SQLite database and tables
when needed.

## Manual Run Instructions

From the project directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then run:

```bash
pip install -r requirements.txt
python run.py
```

---

# API Endpoints

Current implemented endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/api/v1/trips` | Create a trip |
| GET | `/api/v1/trips` | List all trips |
| GET | `/api/v1/trips/<trip_id>` | Get a specific trip |
| PUT | `/api/v1/trips/<trip_id>` | Update a trip |
| DELETE | `/api/v1/trips/<trip_id>` | Delete a trip |

Upcoming endpoints:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/trips/<trip_id>/travelers` | Add traveler |
| DELETE | `/api/v1/trips/<trip_id>/travelers/<traveler_id>` | Remove traveler |
| POST | `/api/v1/trips/<trip_id>/expenses` | Add expense |
| PATCH | `/api/v1/trips/<trip_id>/status` | Change status |
| GET | `/api/v1/trips/<trip_id>/summary` | Trip summary |

---

# Health Check

Request:

```bash
curl -i http://127.0.0.1:5000/health
```

Response:

```json
{
    "status": "ok"
}
```

---

# Trip API Examples

## Create Trip

Request:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips \
-H "Content-Type: application/json" \
-d '
{
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

## Get Trips

Request:

```bash
curl http://127.0.0.1:5000/api/v1/trips
```

Response:

```json
[
 {
  "id":1,
  "destination":"Coxs Bazar",
  "start_date":"2026-12-01",
  "end_date":"2026-12-05",
  "budget":50000,
  "max_travelers":5,
  "status":"PLANNED"
 }
]
```

---

## Database Storage

SQLite data is stored in `instance/trip_planner.db`.
The folder, database, and tables are created automatically on startup.
Existing data is retained across application restarts.