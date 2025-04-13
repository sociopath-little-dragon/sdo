import jwt
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from http import HTTPStatus
from typing import List

from app.core.jwt_handler import decode_access_token
from app.db.db import get_users_by_faculty, get_users_by_group, is_user_enrolled_in_subject, get_username_by_id, \
    get_tasks_by_subject, get_student_labs_by_subject, get_task_data, get_user_solutions_by_task, get_student_labs, \
    get_groups_by_faculty, get_groups_by_user_id
from app.schemas.task import TaskInfo
from app.schemas.teachers import (
    StudentResponse,
    GroupResponse,
    LabResponse,
    LabDetailResponse, CreateLabRequest
)
from app.utils.utils import response_with_json, response_with_error


def get_current_user():
    return "заглушечная"


router = APIRouter(prefix="/api/teachers")


# Получение списка студентов по id факультета
@router.get("/students/{faculty_id}", response_model=List[StudentResponse],
            summary="Получение списка студентов по id факультета")
async def get_students(faculty_id: int):
    students = get_users_by_faculty(faculty_id)
    if isinstance(students, str):
        return response_with_error(
            HTTPStatus.NOT_FOUND,
            students
        )

    serialized_students = [StudentResponse(
        id=student.id,
        full_name=f"{student.last_name} {student.first_name} {student.middle_name}",
        studyGroup=student.studyGroup
    ).model_dump() for student in students]

    return response_with_json(
        HTTPStatus.OK,
        serialized_students
    )


# Получение списка студентов по группе
@router.get("/groups/{group_id}/students", response_model=List[StudentResponse],
            summary="Получение списка студентов по группе")
async def get_students_by_group(group_id: int):
    students = get_users_by_group(group_id)
    if isinstance(students, str):
        return response_with_error(
            HTTPStatus.NOT_FOUND,
            students
        )

    serialized_students: list[StudentResponse] = [StudentResponse(
        id=student.id,
        full_name=f"{student.last_name} {student.first_name} {student.middle_name}",
        studyGroup=student.studyGroup
    ).model_dump() for student in students]

    return response_with_json(
        HTTPStatus.OK,
        serialized_students
    )


# Получение информации о лабораторной работы студента
@router.get("/students/{student_id}/labs/{lab_id}/lab", response_model=LabDetailResponse,
            summary="Получение информации о лабораторной работе студента")
async def get_student_lab_detail(student_id: int, lab_id: int):
    lab = get_student_labs(student_id, lab_id)
    if not lab:
        return response_with_error(
            HTTPStatus.NOT_FOUND,
            "Лабораторная работа не найдена"
        )

    response = LabDetailResponse(
        id=lab.id,
        name=lab.name,
        description=lab.description,
        count_subtasks=lab.count_subtasks,
        status=lab.status,
        solutions=[solution.model_dump() for solution in lab.solutions]
    ).model_dump()

    return response_with_json(
        HTTPStatus.OK,
        response
    )


# Получение лабораторных работ студента
@router.get("/students/{student_id}/subjects/{subject_id}/labs", response_model=list[LabResponse],
            summary="Получение лабораторных работ студента")
async def get_student_tasks(student_id: int, subject_id: int):
    student_username = get_username_by_id(student_id)
    is_enrolled = is_user_enrolled_in_subject(student_username, subject_id)
    if isinstance(is_enrolled, str):
        return response_with_error(
            HTTPStatus.NOT_FOUND,
            is_enrolled
        )

    labs = get_student_labs_by_subject(student_id, subject_id)
    if not labs:
        return response_with_error(
            HTTPStatus.NOT_FOUND,
            "Лабораторные работы не найдены"
        )

    serialized_labs = [LabResponse(
        id=lab.id,
        title=lab.title,
        status=lab.status,
    ).model_dump() for lab in labs]

    return response_with_json(
        HTTPStatus.OK,
        serialized_labs
    )

# Заглушка для получения списка групп факультета
@router.get("/groups/{faculty_id}", response_model=list[GroupResponse], summary="Получение списка групп факультета")
async def get_faculty_groups(faculty_id: int):
    groups = get_groups_by_faculty(faculty_id)
    if isinstance(groups, str):
        return response_with_error(
            HTTPStatus.NOT_FOUND,
            groups
        )

    response: list[GroupResponse] = [
        GroupResponse(
            id=group.id,
            name=group.name,
        ).model_dump() for group in groups
    ]

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=response
    )

# Получение групп преподавателя
@router.get("/groups", response_model=list[GroupResponse], summary="Получение групп преподавателя")
async def get_groups(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"error": "Invalid token format"})
    token = authorization[len("Bearer "):]
    decoded_token = decode_access_token(token)
    if isinstance(decoded_token, str):
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"error": decoded_token})

    user_id = decoded_token.get("user_id")
    groups = get_groups_by_user_id(user_id)

    resposne = [GroupResponse(
        id=group[0],
        name=group[1],
    ).model_dump(
    ) for group in groups]

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=resposne
    )

# Создание лабораторной работы
# @router.post("/create_lab", response_model=int)
# async def create_lab(lab: CreateLabRequest):
