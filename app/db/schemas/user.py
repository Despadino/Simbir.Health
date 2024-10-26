from uuid import UUID
from pydantic import BaseModel, validator, ConfigDict
from typing import List
from datetime import datetime, timedelta
from pydantic_core import ValidationError


class Upgradeuser(BaseModel):
    lastName: str
    firstName: str
    password: str

class UserData(BaseModel):
    lastName: str
    firstName: str
    username: str
    password: str

class AuthenticationsUser(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    refreshToken: str

class UserJWTToken(BaseModel):
    UserJWTToken: str


class FilterData(BaseModel):
    from_is: int
    count: int

class EmployeeRolesModel(BaseModel):
    user_id: str
    roles_id: str

class UpgradeRole(BaseModel):
    lastName: str
    firstName: str
    username: str
    password: str
    roles: List[str]

class DeletedUser(BaseModel):
    is_deleted: bool


class IDRolesModel(BaseModel):
    roles_id: str


class CreateOrUpgradeRoomsData(BaseModel):
    name: str
    hospitals_id: str


class HospitalsModel(BaseModel):
    hospitals_id: str

class CreateOrUpgradeHospitalData(BaseModel):
    name: str
    address: str
    contactPhone: str
    rooms: List[str]

class HospitalData(BaseModel):
    name: str
    address: str
    contactPhone: str



class TimetableData(BaseModel):
    hospital_id: str
    doctor_id: str
    from_datetime: datetime
    to_datetime: datetime
    room: str

    @validator('from_datetime', 'to_datetime', pre=True)
    def validate_iso8601_datetime(cls, value):
        try:
            parsed_datetime = datetime.fromisoformat(value.replace("Z", "+00:00"))
            naive_datetime = parsed_datetime.replace(tzinfo=None)
            return naive_datetime
        except ValueError:
            raise ValueError('Дата и время должны быть в формате ISO 8601')

    @validator('from_datetime', 'to_datetime')
    def validate_minutes_and_seconds(cls, value):
        if value.minute % 30 != 0 or value.second != 0:
            raise ValueError('Минуты должны быть кратны 30, а секунды должны быть равны 0')
        return value

    @validator('to_datetime')
    def validate_datetime_order(cls, value, values):
        if 'from_datetime' in values and value <= values['from_datetime']:
            raise ValueError('to_datetime должно быть больше from_datetime')
        return value

    @validator('to_datetime')
    def validate_datetime_difference(cls, value, values):
        if 'from_datetime' in values and (value - values['from_datetime']) > timedelta(hours=12):
            raise ValueError('Разница между to_datetime и from_datetime не должна превышать 12 часов')
        return value
    

class FromTo(BaseModel):
    from_datetime: str
    to_datetime: str



class AppointmentData(BaseModel):
    timetable_id: str
    time: datetime
    user_id: str

    @validator('time', pre=True)
    def validate_iso8601_datetime(cls, value):
        if isinstance(value, str):
            try:
                # Заменяем "Z" на "+00:00", чтобы корректно интерпретировать временную зону
                if value.endswith('Z'):
                    value = value.replace("Z", "+00:00")
                parsed_datetime = datetime.fromisoformat(value)
                naive_datetime = parsed_datetime.replace(tzinfo=None)
                return naive_datetime
            except ValueError:
                raise ValueError('Дата и время должны быть в формате ISO 8601')
        return value

    @validator('time')
    def validate_minutes_and_seconds(cls, value):
        if value.minute % 30 != 0 or value.second != 0:
            raise ValueError('Минуты должны быть кратны 30, а секунды должны быть равны 0')
        return value
    

    