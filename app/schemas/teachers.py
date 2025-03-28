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