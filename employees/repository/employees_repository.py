import json
import uuid

from datetime import datetime

from employees.repository.models import EmployeesModel, BeneficiariesModel


class EmployeesRepository:

    def __init__(self, session) -> None:
        self.session = session

    async def get(self, employee):
        params = (employee,)
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_getEmployeeByID ?', params)
        results = await cursor.fetchone()
        return json.loads(results[0])[0]

    async def add(self, employee):
        employee['id'] = str(uuid.uuid4())
        employee['create_at'] = datetime.utcnow()
        employee['number_employee'] = str(uuid.uuid4()).split('-')[0].upper()
        employee = EmployeesModel(**employee)
        params = (
            employee.id,
            employee.create_at,
            employee.status,
            employee.name,
            employee.last_name,
            employee.surname,
            employee.birthdate,
            employee.number_employee,
            employee.curp,
            employee.ssn,
            employee.phone,
            employee.nationality
        )

        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_insertEmployees ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', params)
        await self.session.commit()
        return employee

    async def update(self, employee, employee_id):
        employee = EmployeesModel(**employee)
        params = (
            employee_id,
            employee.update_at,
            employee.name,
            employee.last_name,
            employee.surname,
            employee.birthdate,
            employee.number_employee,
            employee.curp,
            employee.ssn,
            employee.phone,
            employee.nationality
        ) 
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_updateEmployee ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', params)
        await self.session.commit()

    async def delete(self, employee):
        params = (employee,)
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_deleteEmployee ?', params)
        await self.session.commit()

    async def list_(self):
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_getEmployees')
        result = await cursor.fetchall()
        if len(result) <= 0:
            return []
        return json.loads(result[0][0])


class BeneficiariesRepository:

    def __init__(self, session) -> None:
        self.session = session

    async def list_(self, employee_id):
        params = (employee_id,)
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_getBeneficiariesByEmployee ?', params)
        result = await cursor.fetchall()
        if len(result) <= 0:
            return []
        return json.loads(result[0][0])

    async def add(self, beneficiarie, employee_id):
        beneficiarie['id'] = str(uuid.uuid4())
        beneficiarie['create_at'] = datetime.utcnow()
        beneficiarie['employee_id'] = employee_id
        beneficiarie = BeneficiariesModel(**beneficiarie)
        params = (
            beneficiarie.id,
            beneficiarie.create_at,
            beneficiarie.status,
            beneficiarie.name,
            beneficiarie.last_name,
            beneficiarie.surname,
            beneficiarie.birthdate,
            beneficiarie.curp,
            beneficiarie.ssn,
            beneficiarie.phone,
            beneficiarie.nationality,
            beneficiarie.participation_percentage,
            beneficiarie.employee_id
        )
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_insertBeneficiarie ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', params)
        await self.session.commit()
        return beneficiarie

    async def delete(self, beneficiarie_id):
        params = (beneficiarie_id,)
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_deleteBeneficiarie ?', params)
        await self.session.commit()

    async def update(self, beneficiarie, beneficiarie_id):
        beneficiarie['id'] = beneficiarie_id
        beneficiarie['update_at'] = datetime.utcnow()
        beneficiarie = BeneficiariesModel(**beneficiarie)
        params = (
            beneficiarie.id,
            beneficiarie.update_at,
            beneficiarie.name,
            beneficiarie.last_name,
            beneficiarie.surname,
            beneficiarie.birthdate,
            beneficiarie.curp,
            beneficiarie.ssn,
            beneficiarie.phone,
            beneficiarie.nationality,
            beneficiarie.participation_percentage
        ) 
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_updateBeneficiarie ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?', params)
        await self.session.commit()
