from datetime import datetime

def validate_trip(data):

    required_fields = ["destination",
    "start_date","end_date",
        "budget","max_travelers"]

    for field in required_fields:
      if field not in data:
            return f"Missing field: {field}"

    try:
        start=datetime.strptime(data["start_date"],"%Y-%m-%d")
        end = datetime.strptime(data["end_date"], "%Y-%m-%d")

        if end<=start:
            return "end_date must be after start_date"

    except ValueError:
          return "Invalid date format"

    try:
       if float(data["budget"])<=0:
          return "Budget must be greater than zero"
    except:
        return "Budget must be numeric"

    try:
       if int(data["max_travelers"]) <= 0:
          return "Capacity must be greater than zero"

    except:
       return "Capacity must be integer"

    return None