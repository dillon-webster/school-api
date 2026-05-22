from sqlmodel import Field, Relationship, SQLModel


# many to many linking table
class StudentCourseLink(SQLModel, table=True):
    student_id: int = Field(primary_key=True, foreign_key="students.student_id")
    course_id: int = Field(primary_key=True, foreign_key="courses.course_id")


class Student(SQLModel, table=True):
    __tablename__ = "students"
    student_id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    courses: list[Course] = Relationship(back_populates="students", link_model=StudentCourseLink)


class Instructor(SQLModel, table=True):
    __tablename__ = "instructors"
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    courses: list["Course"] = Relationship(back_populates="instructor")


class Course(SQLModel, table=True):
    __tablename__ = "courses"
    course_id: int | None = Field(default=None, primary_key=True)
    instructor_id: int = Field(foreign_key="instructors.id")
    instructor: Instructor = Relationship(back_populates="courses")
    title: str
    course_number: str
    credits: int
    students: list[Student] = Relationship(back_populates="courses", link_model=StudentCourseLink)
