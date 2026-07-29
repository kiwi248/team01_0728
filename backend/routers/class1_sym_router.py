from fastapi import APIRouter

from backend.schemas.class1_sym_schema import StudentPublic
from backend.services.class1_sym_service import student_get_all


student = APIRouter()


@student.get("/student/getall")
def get() -> list[StudentPublic]:
    return student_get_all()

