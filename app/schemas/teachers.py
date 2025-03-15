from pydantic import BaseModel
from datetime import datetime


class StudentResponse(BaseModel):
    id: int
    full_name: str
    email: str
    group: str


class GroupResponse(BaseModel):
    group_id: str
    group_name: str


class LabResponse(BaseModel):
    lab_id: int
    title: str
    status: str
    grade: int


class LabDetailResponse(BaseModel):
    lab_id: int
    title: str
    status: str
    grade: int
    submission_date: datetime
    feedback: str
