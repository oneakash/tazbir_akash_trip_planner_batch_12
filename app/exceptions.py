class ApiError(Exception):
    def __init__(self,error,message,status):
        self.error=error
        self.message=message
        self.status=status
        super().__init__(message)