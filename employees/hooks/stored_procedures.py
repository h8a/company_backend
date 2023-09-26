from employees.web.app import app
from employees.repository.unit_of_work import UnitOfWork


@app.on_event('startup')
async def sp_insert_employees():
    async with UnitOfWork() as unit_of_work:
         cursor = await unit_of_work.session.cursor()
         await (await cursor.execute("""
             CREATE OR ALTER PROCEDURE sp_insertEmployees
                @id UNIQUEIDENTIFIER,
                @create_at DATETIME,
                @status VARCHAR(1),
                @name VARCHAR(255),
                @last_name VARCHAR(255),
                @surname VARCHAR(255),
                @birthdate DATE,
                @number_employee VARCHAR(8),
                @curp VARCHAR(18),
                @ssn VARCHAR(11),
                @phone VARCHAR(10),
                @nationality VARCHAR(255)
            AS
            BEGIN
                INSERT INTO employees (id, create_at, status, name, last_name, surname, birthdate, number_employee, curp, ssn, phone, nationality)
                VALUES (@id, @create_at, @status, @name, @last_name, @surname, @birthdate, @number_employee, @curp, @ssn, @phone, @nationality);
            END
        """)).commit()

@app.on_event('startup')
async def sp_get_employee_by_id():
    async with UnitOfWork() as unit_of_work:
         cursor = await unit_of_work.session.cursor()
         await (await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_getEmployeeByID
                @id UNIQUEIDENTIFIER
            AS
            BEGIN
                SELECT 
                    id, create_at, status, name, last_name, surname, birthdate, number_employee, curp, ssn, phone, nationality
                FROM employees
                WHERE id = @id AND status = '1'
                FOR JSON AUTO, INCLUDE_NULL_VALUES;
            END
        """)).commit()

@app.on_event('startup')
async def sp_delete_employee():
    async with UnitOfWork() as unit_of_work:
        cursor = await unit_of_work.session.cursor()
        await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_deleteEmployee
                @id UNIQUEIDENTIFIER
            AS
            BEGIN
                UPDATE employees
                SET status = '0'
                WHERE id = @id;
            END
        """)
        await cursor.commit()

@app.on_event('startup')
async def sp_get_employees():
    async with UnitOfWork() as unit_of_work:
        cursor = await unit_of_work.session.cursor()
        await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_getEmployees
            AS
            BEGIN
                SELECT 
                    id, create_at, update_at, status, name, last_name, surname, birthdate, number_employee, curp, ssn, phone, nationality
                FROM employees
                WHERE status = '1'
                FOR JSON AUTO, INCLUDE_NULL_VALUES;
            END
        """)
        await cursor.commit()

@app.on_event('startup')
async def sp_update_employee():
    async with UnitOfWork() as unit_of_work:
        cursor = await unit_of_work.session.cursor()
        await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_updateEmployee
                @id UNIQUEIDENTIFIER,
                @update_at DATETIME,
                @name VARCHAR(255),
                @last_name VARCHAR(255),
                @surname VARCHAR(255),
                @birthdate DATE,
                @number_employee VARCHAR(8),
                @curp VARCHAR(18),
                @ssn VARCHAR(11),
                @phone VARCHAR(10),
                @nationality VARCHAR(255) 
            AS
            BEGIN
                UPDATE employees
                SET
                    update_at = @update_at, name = @name, last_name = @last_name, surname = @surname, birthdate = @birthdate, number_employee = @number_employee, curp = @curp, ssn = @ssn, phone = @phone, nationality = @nationality
                WHERE
                    id = @id;
            END
        """)
        await cursor.commit()


@app.on_event('startup')
async def sp_get_beneficiaries_by_employee():
    async with UnitOfWork() as unit_of_work:
        cursor = await unit_of_work.session.cursor()
        await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_getBeneficiariesByEmployee
                @employee_id UNIQUEIDENTIFIER
            AS
            BEGIN
                SELECT
                    id, create_at, update_at, status, name, last_name, surname, birthdate, curp, ssn, phone, nationality, participation_percentage 
                FROM beneficiaries
                WHERE
                    status = '1' AND employee_id = @employee_id
                FOR JSON AUTO, INCLUDE_NULL_VALUES;
            END
        """)
        await cursor.commit()

@app.on_event('startup')
async def sp_insert_beneficiarie():
    async with UnitOfWork() as unit_of_work:
        cursor = await unit_of_work.session.cursor()
        await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_insertBeneficiarie
                @id UNIQUEIDENTIFIER,
                @create_at DATETIME,
                @status VARCHAR(1),
                @name VARCHAR(255),
                @last_name VARCHAR(255),
                @surname VARCHAR(255),
                @birthdate DATE,
                @curp VARCHAR(18),
                @ssn VARCHAR(11),
                @phone VARCHAR(10),
                @nationality VARCHAR(255),
                @participation_percentage SMALLINT,
                @employee_id UNIQUEIDENTIFIER
            AS
            BEGIN
                INSERT INTO beneficiaries (id, create_at, status, name, last_name, surname, birthdate, curp, ssn, phone, nationality, participation_percentage, employee_id)
                VALUES (@id, @create_at, @status, @name, @last_name, @surname, @birthdate, @curp, @ssn, @phone, @nationality, @participation_percentage, @employee_id);
            END
        """)
        await cursor.commit()

@app.on_event('startup')
async def sp_delete_beneficiarie():
    async with UnitOfWork() as unit_of_work:
        cursor = await unit_of_work.session.cursor()
        await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_deleteBeneficiarie
                @beneficiarie_id UNIQUEIDENTIFIER
            AS
            BEGIN
                UPDATE beneficiaries
                SET status = '0'
                WHERE id = @beneficiarie_id;
            END
        """)
        await cursor.commit()

@app.on_event('startup')
async def sp_update_beneficiarie():
    async with UnitOfWork() as unit_of_work:
        cursor = await unit_of_work.session.cursor()
        await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_updateBeneficiarie
                @id UNIQUEIDENTIFIER,
                @update_at DATETIME,
                @name VARCHAR(255),
                @last_name VARCHAR(255),
                @surname VARCHAR(255),
                @birthdate DATE,
                @curp VARCHAR(18),
                @ssn VARCHAR(11),
                @phone VARCHAR(10),
                @nationality VARCHAR(255),
                @participation_percentage SMALLINT
            AS
            BEGIN
                UPDATE beneficiaries
                SET
                    update_at = @update_at, name = @name, last_name = @last_name, surname = @surname, birthdate = @birthdate, curp = @curp, ssn = @ssn, phone = @phone, nationality = @nationality, participation_percentage = @participation_percentage
                WHERE
                    id = @id;
            END
        """)
        await cursor.commit()

@app.on_event('startup')
async def sp_get_user_by_username():
    async with UnitOfWork() as unit_of_work:
         cursor = await unit_of_work.session.cursor()
         await (await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_getUserByUsername
                @username VARCHAR(255)
            AS
            BEGIN
                SELECT 
                    id, status, username, password
                FROM users
                WHERE username = @username AND status = '1'
                FOR JSON AUTO, INCLUDE_NULL_VALUES;
            END
        """)).commit()

@app.on_event('startup')
async def sp_get_user_by_id():
    async with UnitOfWork() as unit_of_work:
         cursor = await unit_of_work.session.cursor()
         await (await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_getUserByID
                @user_id UNIQUEIDENTIFIER
            AS
            BEGIN
                SELECT 
                    id, status, username, password
                FROM users
                WHERE id = @user_id AND status = '1'
                FOR JSON AUTO, INCLUDE_NULL_VALUES;
            END
        """)).commit()

@app.on_event('startup')
async def sp_add_user():
    async with UnitOfWork() as unit_of_work:
        cursor = await unit_of_work.session.cursor()
        await cursor.execute("""
            CREATE OR ALTER PROCEDURE sp_insertUser
                @id UNIQUEIDENTIFIER,
                @create_at DATETIME,
                @status VARCHAR(1),
                @username VARCHAR(255),
                @password VARCHAR(255)
            AS
            BEGIN
                INSERT INTO users (id, create_at, status, username, password)
                VALUES (@id, @create_at, @status, @username, @password);
            END
        """)
        await cursor.commit()
