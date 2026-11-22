from pydantic import BaseModel, Field, ConfigDict, EmailStr

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)

class Student(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=16, le=100)
    email: str | None = None

class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    age: int | None = Field(default=None, ge=16, le=100)
    email: str | None = None

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str