from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Extra, conlist, validator


class CreateEmployeeSchema(BaseModel):
    status: Optional[str] = '1'
    name: str
    last_name: str
    surname: Optional[str]
    birthdate: date
    curp: str
    ssn: str
    phone: str
    nationality: str

    class Config:
        extra = Extra.forbid

    @validator("curp")
    def curp_len(cls, value):
        assert len(value) == 18, "Tamaño de CURP invalido"
        return value

    @validator("ssn")
    def ssn_len(cls, value):
        assert len(value) > 11, "Tamaño de SSN invalido"
        return value 


class GetEmployeeSchema(BaseModel):
    id: str
    create_at: Optional[datetime]
    update_at: Optional[datetime] = None
    status: Optional[str] = '1'
    name: str
    last_name: str
    surname: Optional[str]
    birthdate: date
    number_employee: str
    curp: str
    ssn: str
    phone: str
    nationality: str

    class Config:
        extra = Extra.forbid


class GetEmployeesSchema(BaseModel):
    employees: conlist(GetEmployeeSchema)

    class Config:
        extra = Extra.forbid


class UpdateEmployeeSchema(BaseModel):
    update_at: Optional[datetime]
    name: str
    last_name: str
    surname: Optional[str]
    birthdate: date
    number_employee: str
    curp: str
    ssn: str
    phone: str
    nationality: str

    class Config:
        extra = Extra.forbid


class GetBeneficiarieSchema(BaseModel):
    id: str
    create_at: Optional[datetime]
    update_at: Optional[datetime] = None
    status: str
    name: str
    last_name: str
    surname: str
    birthdate: date
    curp: str
    ssn: str
    phone: str
    nationality: str
    participation_percentage: int

    class Config:
        extra = Extra.forbid


class GetBeneficiariesSchema(BaseModel):
    beneficiaries: conlist(GetBeneficiarieSchema)

    class Config:
        extra = Extra.forbid


class CreateBeneficiarieSchema(BaseModel):
    status: Optional[str] = '1'
    name: str
    last_name: str
    surname: Optional[str]
    birthdate: date
    curp: str
    ssn: str
    phone: str
    nationality: str
    participation_percentage: int

    class Config:
        extra = Extra.forbid


class UpdateBeneficiarieSchema(BaseModel):
    update_at: Optional[datetime]
    name: str
    last_name: str
    surname: Optional[str]
    birthdate: date
    curp: str
    ssn: str
    phone: str
    nationality: str
    participation_percentage: int

    class Config:
        extra = Extra.forbid 


class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        extra = Extra.forbid
