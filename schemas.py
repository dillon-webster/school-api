from pydantic import BaseModel


class CreateStudentRequest(BaseModel):
    first_name: str
    last_name: str
    email: str


class CreateStudentResponse(BaseModel):
    student_id: int


class UpdateStudentRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class CreateInstructorRequest(BaseModel):
    first_name: str
    last_name: str
    email: str


class CreateInstructerResponse(BaseModel):
    instructor_id: int


class CreateCourseRequest(BaseModel):
    instructor_id: int
    title: str
    course_number: str
    credits: int


class UpdateInstructorRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class CreateCourseResponse(BaseModel):
    course_id: int


class UpdateCourseRequest(BaseModel):
    instructor_id: int | None = None
    title: str | None = None
    course_number: str | None = None
    credits: int | None = None
