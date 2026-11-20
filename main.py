from fastapi import FastAPI  #import FastAPI class from fastapi module
from routes.students import router as student_router  #import the router from routes/students.py

app = FastAPI()   # Create an instance of the FastAPI class

app.include_router(student_router)  # Include the student router in the main application

@app.get("/")       # called as decorator, it tells FastAPI that when someone sends GET req to root url /, execute the function below.
def home():
    return {"message": "Welcome to Student Management API!"}
