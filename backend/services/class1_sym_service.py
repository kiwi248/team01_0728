from backend.schemas.class1_sym_schema import StudentPublic



def student_get_all() -> list[StudentPublic]:
    return [
        StudentPublic(id=1, subject="Python", score=100),
        StudentPublic(id=2, subject="Streamlit", score=95),
        StudentPublic(id=3, subject="FastAPI", score=90),
        StudentPublic(id=4, subject="Python", score=88),
        StudentPublic(id=5, subject="Streamlit", score=92),
        StudentPublic(id=6, subject="FastAPI", score=85),
        StudentPublic(id=7, subject="Python", score=97),
        StudentPublic(id=8, subject="Streamlit", score=78),
        StudentPublic(id=9, subject="FastAPI", score=83),
        StudentPublic(id=10, subject="Python", score=94),
    ]

