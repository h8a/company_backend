import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, ForeignKey,
    DateTime, Date, SmallInteger
)
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())


class BaseModel:
    id = Column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=generate_uuid)
    create_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, onupdate=datetime.utcnow)
    status = Column(String(1), nullable=False, default='1')


class EmployeesModel(Base, BaseModel):

    __tablename__ = 'employees'

    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    surname = Column(String(255), default='')
    birthdate = Column(Date, nullable=False)
    number_employee = Column(String(8), nullable=False)
    curp = Column(String(18), nullable=False)
    ssn = Column(String(11), nullable=False)
    phone = Column(String(10), nullable=False)
    nationality = Column(String(255), nullable=False)
    beneficiaries = relationship("BeneficiariesModel")

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'create_at': self.create_at.strftime('%Y-%m-%d'),
            'name': self.name,
            'last_name': self.last_name,
            'surname': self.surname,
            'birthdate': self.birthdate.strftime('%Y-%m-%d'),
            'number_employee': self.number_employee,
            'curp': self.curp,
            'ssn': self.ssn,
            'phone': self.phone,
            'nationality': self.nationality,
        }


class BeneficiariesModel(Base, BaseModel):

    __tablename__ = 'beneficiaries'

    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    surname = Column(String(255), default='')
    birthdate = Column(Date, nullable=False)
    curp = Column(String(18), nullable=False)
    ssn = Column(String(11), nullable=False)
    phone = Column(String(10), nullable=False)
    nationality = Column(String(255), nullable=False)  
    participation_percentage = Column(SmallInteger, nullable=False)
    employee_id = Column(ForeignKey("employees.id"), nullable=False)

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'create_at': self.create_at,
            'name': self.name,
            'last_name': self.last_name,
            'surname': self.surname,
            'birthdate': self.birthdate,
            'curp': self.curp,
            'ssn': self.ssn,
            'phone': self.phone,
            'nationality': self.nationality,
            'participation_percentage': self.participation_percentage,
        }


class UsersModel(Base, BaseModel):

    __tablename__ = 'users'

    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': '********'
        }
