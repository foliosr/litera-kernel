import asyncio
from src.controllers.async_controllers import AsyncControllers
from fastapi import APIRouter, HTTPException
from src import schemas

users_router = APIRouter()
users_wish_router = APIRouter


@users_router.get("")
async def get_users(limit: int = 10):
    return await AsyncControllers.cont_select_all_users(limit)


@users_router.get("/{user_id}")
async def get_user(user_id: int):
    res = await AsyncControllers.cont_select_user(user_id)
    return res


@users_router.post("", response_model=schemas.UsersPostDTO, status_code=201)
async def post_user(user_data: schemas.UsersPostDTO):
    res = await AsyncControllers.cont_insert_new_user(user_data)
    if res != 201:
        raise HTTPException(
            status_code=res,
            detail="This email or nickname is already taken"
        )
