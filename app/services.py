from .database import get_connection
from .exceptions import ApiError

def get_trip_or_fail(conn,trip_id):
    trip=conn.execute("SELECT * FROM trips WHERE id=?",(trip_id,)).fetchone()
    if not trip: raise ApiError("TRIP_NOT_FOUND","Trip not found.",404)
    return trip

def get_traveler_count(conn,trip_id):
    return conn.execute(
        "SELECT COUNT(*) FROM trip_travelers WHERE trip_id=?",(trip_id,)
    ).fetchone()[0]

def get_total_expense(conn,trip_id):
    value=conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE trip_id=?",(trip_id,)
    ).fetchone()[0]
    return float(value or 0)

# ---------------- TRIPS ----------------

def create_trip(data):
    conn=get_connection()
    try:
        cur=conn.execute("""
            INSERT INTO trips(destination,start_date,end_date,budget,max_travelers)
            VALUES(?,?,?,?,?)
        """,(data.destination,data.start_date.isoformat(),data.end_date.isoformat(),
             data.budget,data.max_travelers))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def get_all_trips():
    conn=get_connection()
    try:
        return [dict(row) for row in conn.execute("SELECT * FROM trips ORDER BY id").fetchall()]
    finally:
        conn.close()

def get_trip(trip_id):
    conn=get_connection()
    try:
        row=conn.execute("SELECT * FROM trips WHERE id=?",(trip_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def update_trip(trip_id,data):
    conn=get_connection()
    try:
        get_trip_or_fail(conn,trip_id)
        traveler_count=get_traveler_count(conn,trip_id)
        total_expense=get_total_expense(conn,trip_id)

        if data.max_travelers<traveler_count:
            raise ApiError(
                "CAPACITY_CONFLICT",
                "max_travelers cannot be lower than the current traveler count.",
                409
            )

        if data.budget<total_expense:
            raise ApiError(
                "BUDGET_CONFLICT",
                "Budget cannot be lower than current total expenses.",
                409
            )

        conflict=conn.execute("""
            SELECT t2.id
            FROM trip_travelers tt1
            JOIN trip_travelers tt2 ON tt1.traveler_id=tt2.traveler_id
            JOIN trips t2 ON t2.id=tt2.trip_id
            WHERE tt1.trip_id=? AND t2.id<>?
            AND NOT(t2.end_date<? OR t2.start_date>?)
            LIMIT 1
        """,(trip_id,trip_id,data.start_date.isoformat(),data.end_date.isoformat())).fetchone()

        if conflict:
            raise ApiError(
                "OVERLAPPING_TRIP",
                "Updated dates would create an overlapping trip for an existing traveler.",
                409
            )

        conn.execute("""
            UPDATE trips SET destination=?,start_date=?,end_date=?,budget=?,max_travelers=?
            WHERE id=?
        """,(data.destination,data.start_date.isoformat(),data.end_date.isoformat(),
             data.budget,data.max_travelers,trip_id))
        conn.commit()
    finally:
        conn.close()

def delete_trip(trip_id):
    conn=get_connection()
    try:
        get_trip_or_fail(conn,trip_id)
        conn.execute("DELETE FROM trips WHERE id=?",(trip_id,))
        conn.commit()
    finally:
        conn.close()

# ---------------- TRAVELERS ----------------

def add_traveler(trip_id,data):
    conn=get_connection()
    try:
        trip=get_trip_or_fail(conn,trip_id)

        if trip["status"]!="PLANNED":
            raise ApiError(
                "TRIP_NOT_PLANNED",
                "Travelers may only be added to PLANNED trips.",
                409
            )

        existing=conn.execute(
            "SELECT * FROM travelers WHERE email=?",(data.email,)
        ).fetchone()

        if existing:
            duplicate=conn.execute("""
                SELECT 1 FROM trip_travelers
                WHERE trip_id=? AND traveler_id=?
            """,(trip_id,existing["id"])).fetchone()

            if duplicate:
                raise ApiError(
                    "DUPLICATE_TRAVELER",
                    "This traveler is already part of the trip.",
                    409
                )

        if get_traveler_count(conn,trip_id)>=trip["max_travelers"]:
            raise ApiError(
                "TRIP_FULL",
                "The trip has reached its maximum traveler capacity.",
                409
            )

        overlap=conn.execute("""
            SELECT t.id
            FROM travelers tr
            JOIN trip_travelers tt ON tt.traveler_id=tr.id
            JOIN trips t ON t.id=tt.trip_id
            WHERE tr.email=? AND t.id<>?
            AND NOT(t.end_date<? OR t.start_date>?)
            LIMIT 1
        """,(data.email,trip_id,trip["start_date"],trip["end_date"])).fetchone()

        if overlap:
            raise ApiError(
                "OVERLAPPING_TRIP",
                "Traveler already belongs to another trip with overlapping dates.",
                409
            )

        if existing:
            traveler_id=existing["id"]
            conn.execute("UPDATE travelers SET name=? WHERE id=?",(data.name,traveler_id))
        else:
            cur=conn.execute(
                "INSERT INTO travelers(name,email) VALUES(?,?)",(data.name,data.email)
            )
            traveler_id=cur.lastrowid

        conn.execute(
            "INSERT INTO trip_travelers(trip_id,traveler_id) VALUES(?,?)",
            (trip_id,traveler_id)
        )
        conn.commit()
        return traveler_id
    finally:
        conn.close()

def remove_traveler(trip_id,traveler_id):
    conn=get_connection()
    try:
        get_trip_or_fail(conn,trip_id)
        membership=conn.execute("""
            SELECT 1 FROM trip_travelers
            WHERE trip_id=? AND traveler_id=?
        """,(trip_id,traveler_id)).fetchone()

        if not membership:
            raise ApiError(
                "TRAVELER_NOT_FOUND",
                "Traveler is not part of this trip.",
                404
            )

        conn.execute("""
            DELETE FROM trip_travelers
            WHERE trip_id=? AND traveler_id=?
        """,(trip_id,traveler_id))
        conn.commit()
    finally:
        conn.close()

# ---------------- EXPENSES ----------------

def add_expense(trip_id,data):
    conn=get_connection()
    try:
        trip=get_trip_or_fail(conn,trip_id)

        if trip["status"] not in("PLANNED","ONGOING"):
            raise ApiError(
                "EXPENSE_NOT_ALLOWED",
                "Expenses may only be added to PLANNED or ONGOING trips.",
                409
            )

        total=get_total_expense(conn,trip_id)

        if total+data.amount>float(trip["budget"]):
            raise ApiError(
                "BUDGET_EXCEEDED",
                "Expense would exceed the trip budget.",
                409
            )

        cur=conn.execute("""
            INSERT INTO expenses(trip_id,title,amount)
            VALUES(?,?,?)
        """,(trip_id,data.title,data.amount))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

# ---------------- SUMMARY ----------------

def get_trip_summary(trip_id):
    conn=get_connection()
    try:
        trip=get_trip_or_fail(conn,trip_id)
        traveler_count=get_traveler_count(conn,trip_id)
        total_expense=get_total_expense(conn,trip_id)
        return {
            "traveler_count":traveler_count,
            "available_seats":trip["max_travelers"]-traveler_count,
            "total_expense":total_expense,
            "remaining_budget":float(trip["budget"])-total_expense
        }
    finally:
        conn.close()