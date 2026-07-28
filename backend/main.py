from fastapi import FastAPI
from backend.routers.class1_sym_router import student


app = FastAPI(title="Main App")
app.include_router(student)

