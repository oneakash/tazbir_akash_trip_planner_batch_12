import pytest

from app import create_app
from app.database import get_connection
from app.services import create_trip,add_traveler
from app.schemas import TripSchema,TravelerSchema
from app.exceptions import ApiError


@pytest.fixture
def app(monkeypatch,tmp_path):

    test_db=tmp_path/"test.db"

    import app.database as database

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_db
    )

    database.init_db()

    return create_app()


def test_trip_capacity_limit(app):

    trip=TripSchema(
        destination="Coxs Bazar",
        start_date="2026-12-01",
        end_date="2026-12-05",
        budget=50000,
        max_travelers=1
    )

    trip_id=create_trip(trip)

    traveler1=TravelerSchema(
        name="Ayesha",
        email="ayesha@test.com"
    )

    add_traveler(
        trip_id,
        traveler1
    )

    traveler2=TravelerSchema(
        name="Rahim",
        email="rahim@test.com"
    )

    with pytest.raises(ApiError) as error:
        add_traveler(
            trip_id,
            traveler2
        )

    assert error.value.error=="TRIP_FULL"
    assert error.value.status==409