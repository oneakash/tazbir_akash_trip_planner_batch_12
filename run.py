from flask import Flask, jsonify, request
from database import init_db, get_connection
from datetime import datetime

app = Flask(__name__)

init_db()


def error_response(error, message, status):
    return jsonify({
        "error": error,
        "message": message
    }), status


def validate_trip_data(data):
    required = [
        "destination",
        "start_date",
        "end_date",
        "budget",
        "max_travelers"
    ]

    for field in required:
        if field not in data:
            return f"Missing field: {field}"

    try:
        start = datetime.strptime(
            data["start_date"],
            "%Y-%m-%d"
        )

        end = datetime.strptime(
            data["end_date"],
            "%Y-%m-%d"
        )

        if end <= start:
            return "end_date must be after start_date"

    except ValueError:
        return "Dates must use YYYY-MM-DD format"


    try:
        if float(data["budget"]) <= 0:
            return "Budget must be greater than zero"
    except:
        return "Budget must be a number"


    try:
        if int(data["max_travelers"]) <= 0:
            return "Capacity must be greater than zero"
    except:
        return "Capacity must be an integer"


    return None



@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200



# CREATE TRIP
@app.post("/api/v1/trips")
def create_trip():

    data = request.get_json()

    if not data:
        return error_response(
            "INVALID_JSON",
            "Request body must contain JSON data.",
            400
        )


    error = validate_trip_data(data)

    if error:
        return error_response(
            "VALIDATION_ERROR",
            error,
            400
        )


    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO trips
        (
            destination,
            start_date,
            end_date,
            budget,
            max_travelers
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["destination"],
            data["start_date"],
            data["end_date"],
            data["budget"],
            data["max_travelers"]
        )
    )

    connection.commit()

    trip_id = cursor.lastrowid

    connection.close()


    return jsonify({
        "id": trip_id,
        "message": "Trip created successfully"
    }), 201



# READ ALL
@app.get("/api/v1/trips")
def get_trips():

    connection = get_connection()

    trips = connection.execute(
        "SELECT * FROM trips"
    ).fetchall()

    connection.close()

    return jsonify([
        dict(trip)
        for trip in trips
    ]), 200



# READ ONE
@app.get("/api/v1/trips/<int:trip_id>")
def get_trip(trip_id):

    connection = get_connection()

    trip = connection.execute(
        "SELECT * FROM trips WHERE id=?",
        (trip_id,)
    ).fetchone()

    connection.close()


    if not trip:
        return error_response(
            "NOT_FOUND",
            "Trip not found.",
            404
        )


    return jsonify(dict(trip)), 200



# UPDATE
@app.put("/api/v1/trips/<int:trip_id>")
def update_trip(trip_id):

    data = request.get_json()

    error = validate_trip_data(data)

    if error:
        return error_response(
            "VALIDATION_ERROR",
            error,
            400
        )


    connection = get_connection()

    existing = connection.execute(
        "SELECT * FROM trips WHERE id=?",
        (trip_id,)
    ).fetchone()


    if not existing:
        connection.close()

        return error_response(
            "NOT_FOUND",
            "Trip not found.",
            404
        )


    connection.execute(
        """
        UPDATE trips SET
        destination=?,
        start_date=?,
        end_date=?,
        budget=?,
        max_travelers=?
        WHERE id=?
        """,
        (
            data["destination"],
            data["start_date"],
            data["end_date"],
            data["budget"],
            data["max_travelers"],
            trip_id
        )
    )

    connection.commit()
    connection.close()


    return jsonify({
        "message": "Trip updated successfully"
    }), 200



# DELETE
@app.delete("/api/v1/trips/<int:trip_id>")
def delete_trip(trip_id):

    connection = get_connection()

    result = connection.execute(
        "DELETE FROM trips WHERE id=?",
        (trip_id,)
    )

    connection.commit()

    deleted = result.rowcount

    connection.close()


    if deleted == 0:
        return error_response(
            "NOT_FOUND",
            "Trip not found.",
            404
        )


    return jsonify({
        "message": "Trip deleted successfully"
    }), 200



if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000
    )