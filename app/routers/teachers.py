from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from http import HTTPStatus
from typing import List

from sqlalchemy.sql.functions import current_user

from app.schemas.teachers import (
    StudentResponse,
    GroupResponse,
    LabResponse,
    LabDetailResponse
)


def get_current_user():
    return "заглушечная"


router = APIRouter(prefix="/api/teachers")


# Заглушка для получения списка студентов факультета
@router.get("/students", response_model=List[StudentResponse], summary="Получение списка студентов своего факультета")
async def get_students(current_user: dict = Depends(get_current_user)):
    # Заглушка: возвращаем тестовые данные
    students = [
        {
            "id": 1,
            "full_name": "Иванов Иван Иванович",
            "email": "ivanov@example.com",
            "group": "CS-101"
        },
        {
            "id": 2,
            "full_name": "Петров Петр Петрович",
            "email": "petrov@example.com",
            "group": "CS-102"
        }
    ]
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=students
    )


# Заглушка для получения списка студентов по группе
@router.get("/groups/{group_id}/students", response_model=List[StudentResponse],
            summary="Получение списка студентов по группе")
async def get_students_by_group(group_id: str, current_user: dict = Depends(get_current_user)):
    # Заглушка: возвращаем тестовые данные
    students = [
        {
            "id": 2,
            "full_name": "Петров Петр Петрович",
            "email": "petrov@example.com"
        }
    ]
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=students
    )


# Заглушка для получения списка лабораторных работ студента
@router.get("/students/{student_id}/labs", response_model=List[LabResponse],
            summary="Получение списка лабораторных работ студента")
async def get_student_labs(student_id: int, current_user: dict = Depends(get_current_user)):
    # Заглушка: возвращаем тестовые данные
    labs = [
        {
            "lab_id": 5,
            "title": "Лабораторная работа 1",
            "status": "checked",
            "grade": 85
        }
    ]
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=labs
    )


# Заглушка для получения информации о конкретной лабораторной работе студента
@router.get("/students/{student_id}/labs/{lab_id}", response_model=LabDetailResponse,
            summary="Получение информации о лабораторной работе студента")
async def get_student_lab_detail(student_id: int, lab_id: int, current_user: dict = Depends(get_current_user)):
    # Заглушка: возвращаем тестовые данные
    lab_detail = {
        "lab_id": 5,
        "title": "Лабораторная работа 1",
        "status": "checked",
        "grade": 85,
        "submission_date": "2025-02-25T12:00:00",
        "feedback": "Код написан хорошо, но есть проблемы с форматированием."
    }
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=lab_detail
    )


# Заглушка для получения списка групп факультета
@router.get("/groups", response_model=List[GroupResponse], summary="Получение списка групп факультета")
async def get_faculty_groups(current_user: dict = Depends(get_current_user)):
    # Заглушка: возвращаем тестовые данные
    groups = [
        {
            "group_id": "CS-101",
            "group_name": "Computer Science 101"
        },
        {
            "group_id": "CS-102",
            "group_name": "Computer Science 102"
        }
    ]
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=groups
    )
