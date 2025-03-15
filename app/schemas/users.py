from pydantic import BaseModel


class User(BaseModel):
    first_name: str = ""
    last_name: str = ""
    middle_name: str = ""
    username: str = ""
    password: str = ""
    roleType: str = "-"
    studyGroup: str = "-"
    form_education: str = "-"
    faculty: str = "-"


class UserStatus(BaseModel):
    status: str
