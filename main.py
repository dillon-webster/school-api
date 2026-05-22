from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import get_db
from models import Course, Instructor, Student, StudentCourseLink
from schemas import (
    CreateCourseRequest,
    CreateCourseResponse,
    CreateInstructerResponse,
    CreateInstructorRequest,
    CreateStudentRequest,
    CreateStudentResponse,
    UpdateStudentRequest,
    UpdateInstructorRequest,
    UpdateCourseRequest,
)

app = FastAPI()


@app.get("/students")
async def get_students(db: Session = Depends(get_db)) -> list[Student]:
    return db.exec(select(Student)).all()


@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(new_student: CreateStudentRequest, db: Session = Depends(get_db)):
    student = Student(**new_student.model_dump())
    db.add(student)
    db.commit()
    return CreateStudentResponse(student_id=student.student_id)


@app.post("/students/{student_id}", status_code=status.HTTP_201_CREATED)
async def add_student_to_course(student_id: int, course_id: int, db: Session = Depends(get_db)) -> None:
    student: Student | None = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    course: Course | None = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found")

    student.courses.append(course)


@app.patch("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(student_id: int, update_request: UpdateStudentRequest, db: Session = Depends(get_db)) -> None:
    student: Student | None = db.get(Student, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found")

    if update_request.first_name:
        student.first_name = update_request.first_name
    if update_request.last_name:
        student.last_name = update_request.last_name
    if update_request.email:
        student.email = update_request.email

    db.commit()


@app.get("/students/{student_id}/courses")
def get_student_courses(student_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    student: Student | None = db.get(Student, student_id)
    courses: dict[str, str] = {}
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"student with ID {student_id} not found",
        )
    for course in student.courses:
        courses[course.course_number] = course.title

    return courses


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    student: Student | None = db.get(Student, student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"student with ID {student_id} not found",
        )
    db.delete(student)
    db.commit()


@app.get("/instructors")
async def get_instructors(db: Session = Depends(get_db)) -> list[Instructor]:
    return db.exec(select(Instructor)).all()


@app.get("/instructos/{id}/courses")
async def get_instructors_course(id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    instructor: Instructor | None = db.get(Instructor, id)
    if instructor is None:
        raise HTTPException(status_code=404, detail=f"Instructor with ID {id} not found")
    course_desc: dict[str, str] = {}
    for course in instructor.courses:
        course_desc[course.course_number] = course.title

    return course_desc


@app.get("/instructors/{id}/num-courses")
async def get_number_of_course(id: int, db: Session = Depends(get_db)) -> int:
    instructor: Instructor | None = db.get(Instructor, id)
    if instructor is None:
        raise HTTPException(status_code=404, detail=f"Instructor with Id {id} not found")
    return len(instructor.courses)


@app.post("/instructors", status_code=status.HTTP_201_CREATED)
async def create_instructors(new_instructor: CreateInstructorRequest, db: Session = Depends(get_db)):
    instructor = Instructor(**new_instructor.model_dump())
    db.add(instructor)
    db.commit()
    return CreateInstructerResponse(instructor_id=instructor.id)


@app.patch("/instructors/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_instructors(id: int, update_request: UpdateInstructorRequest, db: Session = Depends(get_db)) -> None:
    instructor: Instructor | None = db.get(Instructor, id)
    if instructor is None:
        raise HTTPException(status_code=404, detail=f"Instructor with ID {id} not found")

    for k, v in update_request.model_dump(exclude_unset=True).items():
        setattr(instructor, k, v)

    db.commit()


@app.delete("/instructors/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    instructor: Instructor | None = db.get(Instructor, instructor_id)
    if instructor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"instructor with ID {instructor_id} not found",
        )
    db.delete(instructor)
    db.commit()


@app.get("/courses")
async def get_courses(db: Session = Depends(get_db)) -> list[Course]:
    return db.exec(select(Course)).all()


@app.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_courses(new_course: CreateCourseRequest, db: Session = Depends(get_db)):
    course = Course(**new_course.model_dump())
    db.add(course)
    db.commit()
    return CreateCourseResponse(course_id=course.course_id)


@app.patch("/courses/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_courses(id: int, update_request: UpdateCourseRequest, db: Session = Depends(get_db)) -> None:
    course: Course | None = db.get(Course, id)
    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with ID {id} not found")

    for k, v in update_request.model_dump(exclude_unset=True).items():
        setattr(course, k, v)

    db.commit()


@app.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    course: Course | None = db.get(Course, course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"course with ID {course_id} not found",
        )
    db.delete(course)
    db.commit()
