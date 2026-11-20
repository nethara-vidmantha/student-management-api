from pydantic import BaseModel, Field

class Student(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=16, le=100)
    email: str | None = None

class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    age: int | None = Field(default=None, ge=16, le=100)
    email: str | None = None