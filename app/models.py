class Trip:

    def __init__(
        self,
        id,
        destination,
        start_date,
        end_date,
        budget,
        max_travelers,
        status
    ):

        self.id = id
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.max_travelers = max_travelers
        self.status = status


    def to_dict(self):

        return {

            "id": self.id,

            "destination": self.destination,

            "start_date": self.start_date,

            "end_date": self.end_date,

            "budget": self.budget,

            "max_travelers": self.max_travelers,

            "status": self.status
        }