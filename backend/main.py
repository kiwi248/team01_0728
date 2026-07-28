from fastapi import FastAPI
from backend.routers import class1_sym_router
from backend.routers import class2_inhye_router


app = FastAPI(title="1반, 2반 학생점수관리페이지", description="학생점수관리페이지 API 문서", version="1.0.0")

app.include_router(class1_sym_router)
app.include_router(class2_inhye_router)