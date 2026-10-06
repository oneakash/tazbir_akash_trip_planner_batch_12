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

## Health Check

```bash
curl -i http://127.0.0.1:5000/health
```

Successful response: HTTP 200 with:

```json
{"status": "ok"}
```

## Database Storage

SQLite data is stored in `instance/trip_planner.db`.
The folder, database, and tables are created automatically on startup.
Existing data is retained across application restarts.