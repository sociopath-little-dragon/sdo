from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from http import HTTPStatus

from app.core.check_auth import check_auth

from app.db.db import get_user_subjects, is_user_enrolled_in_subject, get_tasks_by_subject
from app.schemas.subject import SubjectInfo
from app.schemas.task import Task

router = APIRouter()


# return user subjects [[1, "Python", 5], [2, "C++", 7]] or "Subjects not found" | [id, name, grade]
@router.get("/subjects", response_model=list[SubjectInfo], summary="Получение всех предметов пользователя")
async def get_subjects(authorization: str = Header(...)) -> JSONResponse:
    check_data = check_auth(authorization)
    if isinstance(check_data, JSONResponse):
        return check_data

    user_subjects = get_user_subjects(check_data['username'])

    serialized_subjects = [subject.model_dump() for subject in user_subjects]

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=serialized_subjects
    )

# return tasks of subject by subject_id
@router.get("/tasks/{subject_identifier}", response_model=list[Task], summary="Получение лабораторных работ предмета")
async def get_tasks(subject_identifier: str, authorization: str = Header(...)) -> JSONResponse:
    check_data = check_auth(authorization)
    if isinstance(check_data, JSONResponse):
        return check_data

    user_subjects = is_user_enrolled_in_subject(check_data['username'], subject_identifier)

    # Если пользователь не прикреплен к дисциплине или дисциплина не найдена
    if isinstance(user_subjects, str):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"error": user_subjects}
        )

    subject_tasks = get_tasks_by_subject(subject_identifier)

    serialized_tasks = [task.model_dump() for task in subject_tasks]

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=serialized_tasks
    )
