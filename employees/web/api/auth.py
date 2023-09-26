from datetime import datetime, timedelta

from fastapi import status, HTTPException
from employees.repository.auth_repository import AuthRepository
from employees.repository.unit_of_work import UnitOfWork
from employees.web.app import app
from employees.web.api.schemas import LoginSchema

@app.post('/auth/login', status_code=status.HTTP_202_ACCEPTED)
async def login_user(payload: LoginSchema):
    async with UnitOfWork() as unit_of_work:
        user = AuthRepository(unit_of_work.session)
        payload_user = payload.dict()
        user_db = await user.get_by_username(payload_user.get('username'))
        if len(user_db) <= 0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not user.valid_user(payload_user.get('password'), user_db.get('password')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        token = user.generate_token(
            payload={
                'id': user_db.get('id'),
                'exp': datetime.utcnow() + timedelta(minutes=60*24),
            }
        )
        return {
            'id': user_db.get('id'),
            'username': user_db.get('username'),
            'token': token
        }

@app.post('/auth/register', status_code=status.HTTP_202_ACCEPTED)
async def register_user(payload: LoginSchema):
    async with UnitOfWork() as unit_of_work:
        user = AuthRepository(unit_of_work.session)
        user = await user.add(payload.dict())
    return user.as_dict
