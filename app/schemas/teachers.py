from pydantic import BaseModel

from app.schemas.task import SolutionInfo


class StudentResponse(BaseModel):
    id: int = 0
    full_name: str = "Не указано"
    studyGroup: str = "Не указано"

class GroupResponse(BaseModel):
    id: int = 0
    name: str = ""


class LabResponse(BaseModel):
    id: int = 0
    title: str = ""
    status: str = ""


class LabDetailResponse(BaseModel):
    id: int = 0
    name: str = ""
    description: str = ""
    count_subtasks: int = 0
    status: str = ""
    solutions: list[SolutionInfo] = []


class GroupResponse(BaseModel):
    id: int
    name: str = ""


class TestCase(BaseModel):
    input: str
    output: str


class CreateLabRequest(BaseModel):
    title: str = ""
    description: str = ""
    subject_id: int = 0
    formula: str = ""
    variables: str = ""
    test_cases: list[TestCase] = []


# class CreateLabResponse(BaseModel):
