from flask import jsonify,request
from pydantic import ValidationError
from .schemas import TripSchema,TravelerSchema,ExpenseSchema
from .services import (
    create_trip,get_all_trips,get_trip,update_trip,delete_trip,
    add_traveler,remove_traveler,add_expense,get_trip_summary
)
from .exceptions import ApiError

def parse_json(schema):
    data=request.get_json(silent=True)
    if data is None:
        raise ApiError("INVALID_JSON","Request body must contain valid JSON.",400)
    try:
        return schema.model_validate(data)
    except ValidationError as e:
        err=e.errors()[0]
        field=".".join(str(x) for x in err["loc"])
        message=err["msg"]
        raise ApiError(
            "VALIDATION_ERROR",
            f"{field}: {message}" if field else message,
            400
        )

def register_routes(app):

    @app.errorhandler(ApiError)
    def handle_api_error(e):
        return jsonify({"error":e.error,"message":e.message}),e.status

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error":"NOT_FOUND","message":"Resource not found."}),404

    @app.get("/health")
    def health():
        return jsonify({"status":"ok"}),200

    @app.post("/api/v1/trips")
    def create_trip_route():
        data=parse_json(TripSchema)
        trip_id=create_trip(data)
        return jsonify({"id":trip_id,"message":"Trip created successfully"}),201

    @app.get("/api/v1/trips")
    def list_trips():
        return jsonify(get_all_trips()),200

    @app.get("/api/v1/trips/<int:trip_id>")
    def single_trip(trip_id):
        trip=get_trip(trip_id)
        if not trip:
            raise ApiError("TRIP_NOT_FOUND","Trip not found.",404)
        return jsonify(trip),200

    @app.put("/api/v1/trips/<int:trip_id>")
    def update_trip_route(trip_id):
        data=parse_json(TripSchema)
        update_trip(trip_id,data)
        return jsonify({"message":"Trip updated successfully"}),200

    @app.delete("/api/v1/trips/<int:trip_id>")
    def delete_trip_route(trip_id):
        delete_trip(trip_id)
        return jsonify({"message":"Trip deleted successfully"}),200

    @app.post("/api/v1/trips/<int:trip_id>/travelers")
    def add_traveler_route(trip_id):
        data=parse_json(TravelerSchema)
        traveler_id=add_traveler(trip_id,data)
        return jsonify({
            "id":traveler_id,
            "message":"Traveler added successfully"
        }),201

    @app.delete("/api/v1/trips/<int:trip_id>/travelers/<int:traveler_id>")
    def remove_traveler_route(trip_id,traveler_id):
        remove_traveler(trip_id,traveler_id)
        return jsonify({"message":"Traveler removed successfully"}),200

    @app.post("/api/v1/trips/<int:trip_id>/expenses")
    def add_expense_route(trip_id):
        data=parse_json(ExpenseSchema)
        expense_id=add_expense(trip_id,data)
        return jsonify({
            "id":expense_id,
            "message":"Expense added successfully"
        }),201

    @app.get("/api/v1/trips/<int:trip_id>/summary")
    def summary_route(trip_id):
        return jsonify(get_trip_summary(trip_id)),200