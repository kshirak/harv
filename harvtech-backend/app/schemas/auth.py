from typing import Union

from pydantic import BaseModel, ConfigDict, StrictInt, field_validator


class UserRegister(BaseModel):
    name: str
    place: str
    aadhar_number: str
    phone_number: str
    location: str
    acres_of_land: float
    password: Union[StrictInt, str]

    model_config = ConfigDict(extra="forbid")

    @field_validator("aadhar_number")
    @classmethod
    def validate_aadhar_number(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 12:
            raise ValueError("Aadhar number must be exactly 12 digits")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not value.isdigit() or len(value) < 10:
            raise ValueError("Phone number must contain at least 10 digits")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: Union[int, str]) -> int:
        if isinstance(value, str):
            if not value.isdigit():
                raise ValueError("Password must be exactly 4 digits")
            value = int(value)
        if value < 1000 or value > 9999:
            raise ValueError("Password must be exactly 4 digits")
        return value


class UserLogin(BaseModel):
    fin_id: str
    password: Union[StrictInt, str]


class Token(BaseModel):
    access_token: str
    token_type: str