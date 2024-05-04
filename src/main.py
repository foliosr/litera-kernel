import asyncio
import os
import sys
from typing import Optional

from src.schemas import *

import uvicorn
from fastapi import FastAPI
from src.controllers.async_controllers import AsyncControllers
from src.queries.async_orm import AsyncORM
from src.routers.users import users_router

sys.path.insert(1, os.path.join(sys.path[0], '..'))

app = FastAPI()


app.include_router(
    users_router,
    prefix='/users'
)




