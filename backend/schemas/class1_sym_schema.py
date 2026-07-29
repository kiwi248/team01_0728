from pydantic import BaseModel, Field

class StudentPublic(BaseModel):
    id : int
    subject : str
    score : int

