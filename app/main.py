from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Student Management API")


# Student Model
class Student(BaseModel):
    id: int
    name: str
    department: str
    semester: int = Field(..., ge=1, le=12)
    cgpa: float = Field(..., ge=0.0, le=4.0)


# In-memory database
students = {}


# GET - Get all students
@app.get("/students")
def get_students():
    return list(students.values())


# GET - Get student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return students[student_id]


# POST - Create student
@app.post("/students", status_code=201)
def create_student(student: Student):

    if student.id in students:
        raise HTTPException(
            status_code=400,
            detail="Student ID already exists"
        )

    students[student.id] = student

    return student


# PUT - Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if student.id != student_id:
        raise HTTPException(
            status_code=400,
            detail="Student ID mismatch"
        )

    students[student_id] = student

    return student


# DELETE - Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    deleted_student = students.pop(student_id)

    return {
        "message": "Student deleted successfully",
        "student": deleted_student
    }