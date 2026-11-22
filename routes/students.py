from fastapi import APIRouter, HTTPException, Depends
from dependencies import StudentNotFoundException
from models import Student, StudentUpdate
from models import Student, StudentUpdate, StudentResponse
from dependencies import get_current_user

from sqlalchemy.orm import Session

from database import get_db
from db_models import StudentDB
from dependencies import get_admin_user

router = APIRouter()

@router.get("/students", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    students = db.query(StudentDB).all()
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

@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if student is None:
        raise StudentNotFoundException()

    return student



@router.patch("/students/{student_id}", response_model=StudentResponse)
def patch_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
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

    return student

@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    updated_student: Student,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
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
    student.email = updated_student.email

    db.commit()
    db.refresh(student)

    return student

@router.delete(
    "/students/{student_id}",
    status_code=204
)
def delete_student(student_id: int, db: Session = Depends(get_db), current_user = Depends(get_admin_user)):

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
    db.refresh(student)
    return None


@router.post(
    "/students",
    response_model=StudentResponse,
    status_code=201
)
def add_student(student: Student, db: Session = Depends(get_db), current_user = Depends(get_admin_user)):

    new_student = StudentDB(
    name=student.name,
    age=student.age,
    email=student.email
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student