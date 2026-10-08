from datetime import date
from pydantic import BaseModel,Field,field_validator,model_validator

class StatusSchema(BaseModel):
    status:str

class TripSchema(BaseModel):
    destination:str=Field(min_length=1)
    start_date:date
    end_date:date
    budget:float=Field(gt=0)
    max_travelers:int=Field(gt=0)

    @field_validator("destination")
    @classmethod
    def clean_destination(cls,v):
        v=v.strip()
        if not v: raise ValueError("destination cannot be empty")
        return v

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date<=self.start_date:
            raise ValueError("end_date must be later than start_date")
        return self

class TravelerSchema(BaseModel):
    name:str=Field(min_length=1)
    email:str=Field(min_length=3)

    @field_validator("name")
    @classmethod
    def clean_name(cls,v):
        v=v.strip()
        if not v: raise ValueError("name cannot be empty")
        return v

    @field_validator("email")
    @classmethod
    def clean_email(cls,v):
        v=v.strip().lower()
        if "@" not in v or v.startswith("@") or v.endswith("@"):
            raise ValueError("invalid email")
        return v

class ExpenseSchema(BaseModel):
    title:str=Field(min_length=1)
    amount:float=Field(gt=0)

    @field_validator("title")
    @classmethod
    def clean_title(cls,v):
        v=v.strip()
        if not v: raise ValueError("title cannot be empty")
        return v