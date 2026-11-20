
from fastapi import FastAPI, HTTPException  #import FastAPI class from fastapi module
from pydantic import BaseModel, Field

app = FastAPI()   # Create an instance of the FastAPI class

class Student(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=16, le=100)

class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    age: int | None = Field(default=None, ge=16, le=100)

@app.get("/")       # called as decorator, it tells FastAPI that when someone sends GET req to root url /, execute the function below.
def home():
    return {"message": "Welcome to Student Management API!"}


students = [
    {"id": 1, "name": "Kamal", "age": 22},
    {"id": 2, "name": "Nimal", "age": 23},
    {"id": 3, "name": "Amali", "age": 21}
]

@app.get("/students")
def get_students():
    return students


@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

@app.patch("/students/{student_id}")
def patch_student(student_id: int, student_update: StudentUpdate):
    for student in students:
        if student["id"] == student_id:

            update_data = student_update.model_dump(exclude_unset=True)

            student.update(update_data)

            return {
                "message": "Student updated successfully",
                "student": student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for student in students:
        if student["id"] == student_id:
            student["name"] = updated_student.name
            student["age"] = updated_student.age

            return {
                "message": "Student updated successfully",
                "student": student
            }

    return {"message": "Student not found"}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)

            return {
                "message": "Student deleted successfully"
            }

    return {"message": "Student not found"}


@app.post("/students")
def add_student(student: Student):
    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "age": student.age
    }

    students.append(new_student)

    return {
        "message": "Student added successfully",
        "student": new_student
    }
