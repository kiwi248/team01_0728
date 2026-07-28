from fastapi import APIRouter
from backend.schemas.class2_inhye_schema import Student2Public
from backend.services.class2_inhye_service import Student2_create,Student2_get_all

Student2_router = APIRouter()

@Student2_router.post("/Student2/create")
def create(Student2:Student2Public) -> Student2Public:
    return Student2_create(Student2)


@Student2_router.get("/product/getall")
def get_all() -> list[Student2Public]:
    return Student2_get_all()