from fastapi import FastAPI  #import FastAPI class from fastapi module
from routes.students import router as student_router  #import the router from routes/students.py
from database import engine, Base
from db_models import StudentDB
import time
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from dependencies import get_app_info

app = FastAPI()   # Create an instance of the FastAPI class

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    print(f"Request: {request.method} {request.url.path}")
    print(f"Processing time: {process_time:.4f} seconds")

    return response

Base.metadata.create_all(bind=engine)

app.include_router(student_router)  # Include the student router in the main application

@app.get("/")       # called as decorator, it tells FastAPI that when someone sends GET req to root url /, execute the function below.
def home():
    return {"message": "Welcome to Student Management API!"}

@app.get("/app-info")
def app_info(info: dict = Depends(get_app_info)):
    return info