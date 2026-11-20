from fastapi import APIRouter, HTTPException
from models import Student, StudentUpdate

router = APIRouter()

students = [
    {"id": 1, "name": "Kamal", "age": 22},
    {"id": 2, "name": "Nimal", "age": 23},
    {"id": 3, "name": "Amali", "age": 21}
]

@router.get("/students")
def get_students():
    return students

@router.get("/students/filter")
def filter_students(min_age: int | None = None):

    if min_age is None:
        return students

    filtered_students = []

    for student in students:
        if student["age"] >= min_age:
            filtered_students.append(student)

    return filtered_students

@router.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )



@router.patch("/students/{student_id}")
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

@router.put("/students/{student_id}")
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

@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)

            return {
                "message": "Student deleted successfully"
            }

    return {"message": "Student not found"}


@router.post("/students")
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