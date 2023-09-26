import json
import uuid
from datetime import datetime

import jwt
from passlib.hash import pbkdf2_sha256
from employees.repository.models import UsersModel
from employees.web.app import settings


class AuthRepository:

    def __init__(self, session=None) -> None:
        self.session = session

    async def add(self, user):
        user['id'] = str(uuid.uuid4())
        user['create_at'] = datetime.utcnow()
        user['status'] = '1'
        user_model = UsersModel(**user)
        params = (
            user_model.id,
            user_model.create_at,
            user_model.status,
            user_model.username,
            pbkdf2_sha256.hash(user_model.password)
        )
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_insertUser ?, ?, ?, ?, ?', params)
        await self.session.commit()
        return user_model

    async def get_by_id(self, user_id):
        params = (user_id,)
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_getUserByID ?', params)
        results = await cursor.fetchone()
        if len(results) <= 0:
            return [] 
        return json.loads(results[0])[0]

    async def get_by_username(self, username):
        params = (username,)
        cursor = await self.session.cursor()
        await cursor.execute('EXEC sp_getUserByUsername ?', params)
        results = await cursor.fetchone()
        if len(results) <= 0:
            return []
        return json.loads(results[0])[0] 

    def generate_token(self, payload, secret=settings.jwt_secret, algorithm='HS256'):
        return jwt.encode(
            payload=payload,
            key=secret,
            algorithm=algorithm
        ) 

    def valid_token(self, token):
        try:
            return jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=['HS256']
            )
        except jwt.InvalidTokenError:
            return None

    def valid_user(self, password_form, password_user):
        if not pbkdf2_sha256.verify(password_form, password_user):
            return None
        return True

