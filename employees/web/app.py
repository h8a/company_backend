from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from employees.web.settings import Settings

from employees.middlewares.auth import AuthorizeRequestMiddleware

settings = Settings()

app = FastAPI()

app.add_middleware(AuthorizeRequestMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from employees.hooks import stored_procedures
from employees.web.api import auth
from employees.web.api import api
