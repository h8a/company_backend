from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends, status, Response, HTTPException, Header, Security
from fastapi.security.api_key import APIKeyHeader 
from employees.web.app import app
from employees.web.api.schemas import (
    CreateEmployeeSchema, GetBeneficiarieSchema, GetEmployeeSchema,
    UpdateEmployeeSchema, CreateBeneficiarieSchema, UpdateBeneficiarieSchema)
from employees.repository.employees_repository import EmployeesRepository, BeneficiariesRepository
from employees.repository.unit_of_work import UnitOfWork


api_key_header = APIKeyHeader(name='Authorization')

@app.get('/employees')
async def get_employees(token: str = Security(api_key_header)):
    async with UnitOfWork() as unit_of_work:
        employee = EmployeesRepository(unit_of_work.session)
        employees = await employee.list_()
    return employees

@app.post('/employees', status_code=status.HTTP_201_CREATED)
async def create_employees(payload: CreateEmployeeSchema, token: str = Security(api_key_header)):
    async with UnitOfWork() as unit_of_work:
        employee = EmployeesRepository(unit_of_work.session)
        await employee.add(payload.dict())
    return ''

@app.get('/employees/{employee_id}', response_model=GetEmployeeSchema)
async def get_employee(employee_id: UUID, token: str = Security(api_key_header)):
    async with UnitOfWork() as unit_of_work:
        employee = EmployeesRepository(unit_of_work.session)
        employee = await employee.get(employee_id)
        return employee

@app.delete('/employees/{employee_id}',
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response)
async def delete_employee(employee_id: UUID, token: str = Security(api_key_header)):
    async with UnitOfWork() as unit_of_work:
        employee = EmployeesRepository(unit_of_work.session)
        await employee.delete(employee_id)
    return

@app.put('/employees/{employee_id}',
         status_code=status.HTTP_204_NO_CONTENT,
         response_class=Response)
async def update_employee(employee_id: UUID, payload: UpdateEmployeeSchema, token: str = Security(api_key_header)):
    async with UnitOfWork() as unit_of_work:
        employee = EmployeesRepository(unit_of_work.session)
        await employee.update(payload.dict(), employee_id)
    return

@app.get('/employees/{employee_id}/beneficiaries')
async def get_beneficiaries(employee_id: UUID, token: str = Security(api_key_header)):
    async with UnitOfWork() as unit_of_work:
        beneficiaries = BeneficiariesRepository(unit_of_work.session)
        employee_beneficiaries = await beneficiaries.list_(employee_id)
        return employee_beneficiaries

@app.post('/employees/{employee_id}/beneficiaries',
          status_code=status.HTTP_201_CREATED,
          response_model=GetBeneficiarieSchema)
async def create_beneficiarie(employee_id: UUID, payload: CreateBeneficiarieSchema, token: str = Security(api_key_header)):
    async with UnitOfWork() as unit_of_work:
        beneficiarie = BeneficiariesRepository(unit_of_work.session)
        beneficiaries_db = await beneficiarie.list_(employee_id)
        print(beneficiaries_db)
        participations = sum([ 
            participation.get('participation_percentage')
            for participation in beneficiaries_db
        ]+[payload.dict().get('participation_percentage')])
        print(participations)
        if participations > 100:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail='Participacion sobrepasada'
            )
        else:
            beneficiarie = await beneficiarie.add(payload.dict(), employee_id)
            return beneficiarie.as_dict

@app.delete('/employees/beneficiaries/{beneficiarie_id}',
            response_class=Response)
async def delete_beneficiarie(beneficiarie_id: UUID, token: str = Security(api_key_header)):
    async with UnitOfWork() as unit_of_work:
        beneficiarie = BeneficiariesRepository(unit_of_work.session)
        await beneficiarie.delete(beneficiarie_id)
    return

@app.put('/employees/beneficiaries/{beneficiarie_id}',
         response_class=Response)
async def update_beneficiarie(beneficiarie_id: UUID, payload: UpdateBeneficiarieSchema, token: str = Security(api_key_header)):
    async with UnitOfWork() as unit_of_work:
        beneficiarie = BeneficiariesRepository(unit_of_work.session)
        await beneficiarie.update(payload.dict(), beneficiarie_id)
    return
