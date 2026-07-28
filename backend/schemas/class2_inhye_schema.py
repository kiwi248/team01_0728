from pydantic import BaseModel, Field

class Student2Public(BaseModel):
    id:int
    name:str
    Korean:int
    English:int
    Math:int