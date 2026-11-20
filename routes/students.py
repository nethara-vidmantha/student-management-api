from fastapi import APIRouter, HTTPException, Depends
from models import Student, StudentUpdate

from sqlalchemy.orm import Session

from database import get_db
from db_models import StudentDB

router = APIRouter()

@router.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(StudentDB).all()     #this is equals to select*from students;

    return students

@router.get("/students/filter")
def filter_students(
    min_age: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(StudentDB)

    if min_age is not None:
        query = query.filter(StudentDB.age >= min_age)

    return query.all()

@router.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student



@router.patch("/students/{student_id}")
def patch_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return {
        "message": "Student updated successfully",
        "student": student
    }

@router.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: Student,
    db: Session = Depends(get_db)
):
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = updated_student.name
    student.age = updated_student.age

    db.commit()
    db.refresh(student)

    return {
        "message": "Student updated successfully",
        "student": student
    }

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }


@router.post("/students")
def add_student(student: Student, db: Session = Depends(get_db)):

    new_student = StudentDB(
        name=student.name,
        age=student.age
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student added successfully",
        "student": new_student
    }