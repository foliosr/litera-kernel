import asyncio
from sqlalchemy import insert, select, update, func, or_, and_
from sqlalchemy.orm import selectinload, joinedload
from src.database import async_session_factory
from src.secure import Secure
from src.models import *
from src import schemas
from src.queries.async_orm import AsyncORM
from src.queries.orm import ConvertDTO


class AsyncControllers:

    @staticmethod
    async def cont_insert_new_user(user: schemas.UsersPostDTO):
        query = (
            select(UsersModel)
            .filter(UsersModel.id == user.email)
        )
        async with async_session_factory() as session:
            alr_email = await session.execute(query)
        if alr_email.first() is None:
            query = (
                    select(UsersModel)
                    .filter(UsersModel.nickname == user.nickname)
            )
            async with async_session_factory() as session:
                alr_nickname = await session.execute(query)
            if alr_nickname.first() is None:
                await AsyncORM.insert_user_bookshelf(user)
                return 201
            else:
                return 409
        else:
            return 409

    @staticmethod
    async def cont_insert_user_bookshelf(bookshelf: schemas.UsersBookshelfPostDTO, auth_user_id: int):
        if bookshelf.user_id == auth_user_id:
            user_id = bookshelf.user_id
            query = (
                select(UsersBookcaseModel)
                .filter(UsersBookcaseModel.user_id == user_id)
            )
            async with async_session_factory() as session:
                alr_bookshelf = await session.execute(query)
            if alr_bookshelf.first() is None:
                await AsyncORM.insert_user_bookshelf(bookshelf)
                return True
        else:
            return False

    @staticmethod
    async def cont_insert_user_favorite_post(post: schemas.UsersFavouritesPostsPostDTO, auth_user_id: int):
        if auth_user_id == post.user_id:
            async with async_session_factory() as session:
                query = (
                    select(UsersFavouritesPostsModel)
                    .filter(and_(UsersFavouritesPostsModel.user_id == post.user_id, UsersFavouritesPostsModel.post_id == post.post_id))
                )
                alr_post = await session.execute(query)
            if alr_post.first() is None:
                await AsyncORM.insert_user_favorite_post(post)
                return True
        else:
            return False

    @staticmethod
    async def cont_delete_user_favorite_post(user_id: int, post_id: int, auth_user_id: int):
        if auth_user_id == user_id:
            await AsyncORM.delete_user_favorite_post(user_id, post_id)
            return True
        else:
            return False

    @staticmethod
    async def cont_insert_user_favorite_tag(tag: schemas.UsersFavouritesTagsPostDTO, auth_user_id):
        if tag.user_id == auth_user_id:
            async with async_session_factory() as session:
                query = (
                    select(TagsModel)
                    .filter(TagsModel.id == tag.tag_id)
                )
                dec_tag = await session.execute(query)
            if dec_tag.first() is not None:
                async with async_session_factory() as session:
                    query = (
                        select(UsersFavouritesTags)
                        .filter(and_(UsersFavouritesTags.user_id == tag.user_id,
                                     UsersFavouritesTags.tag_id == tag.tag_id))
                    )
                    alr_tag = await session.execute(query)
                if alr_tag.first() is None:
                    await AsyncORM.insert_user_favorite_tag(tag)
                return True
        else:
            return False

    @staticmethod
    async def cont_delete_user_favorite_tag(user_id: int, tag_id: int, auth_user_id):
        if user_id == auth_user_id:
            await AsyncORM.delete_user_favorite_tag(user_id, tag_id)
            return True
        else:
            return False

    @staticmethod
    async def cont_insert_user_wish(wish: schemas.UsersWishlistsPostDTO, auth_user_id):
        if wish.user_id == auth_user_id:
            async with async_session_factory() as session:
                query = (
                    select(UsersWishlistsModel)
                    .filter(and_(UsersWishlistsModel.user_id == wish.user_id, UsersWishlistsModel.product_id == wish.product_id))
                )
                alr_wish = await session.execute(query)
            if alr_wish.first() is None:
                await AsyncORM.insert_user_wish(wish)
                return True
        else:
            return False

    @staticmethod
    async def cont_delete_user_wish(user_id: int, product_id: int, auth_user_id):
        if user_id == auth_user_id:
            await AsyncORM.delete_user_wish(user_id, product_id)
            return True
        else:
            return False

    @staticmethod
    async def cont_insert_user_subscription(subscription: schemas.ChannelsSubscriptionsPostDTO, auth_user_id: int):
        if subscription.user_id == auth_user_id:
            async with async_session_factory() as session:
                query = (
                    select(ChannelsSubscriptionsModel)
                    .filter(and_(ChannelsSubscriptionsModel.user_id == subscription.user_id,
                                 ChannelsSubscriptionsModel.channel_id == subscription.channel_id))
                )
                alr_sub = await session.execute(query)
                if alr_sub.first() is None:
                    await AsyncORM.insert_user_subscription(subscription)
                    return True
        else:
            return False

    @staticmethod
    async def cont_delete_user_subscription(user_id: int, channel_id: int, auth_user_id: int):
        if user_id == auth_user_id:
            await AsyncORM.delete_user_subscription(user_id, channel_id)
            return True
        else:
            return False

    @staticmethod
    async def cont_select_all_users(limit: int):
        res = await AsyncORM.select_all_users(limit)
        users = ConvertDTO.convert_to_dto(schemas.UsersShortDTO, res)
        return users

    @staticmethod
    async def cont_find_users(key_word: str):
        res = await AsyncORM.find_users(key_word)
        users = ConvertDTO.convert_to_dto(schemas.UsersShortDTO, res)
        return users

    @staticmethod
    async def cont_select_full_user(user_id: int, auth_user_id):
        if user_id == auth_user_id:
            res = await AsyncORM.select_full_user(user_id)
            user = ConvertDTO.convert_to_dto(schemas.UsersRelDTO, res)
            return user

    @staticmethod
    async def cont_select_user(user_id: int, auth_user_id=0):
        if user_id == auth_user_id:
            res = await AsyncORM.select_full_user(user_id)
            user = ConvertDTO.convert_to_dto(schemas.UsersDTO, res)
            return user
        else:
            res = await AsyncORM.select_user(user_id)
            user = ConvertDTO.convert_to_dto(schemas.UsersShortDTO, res)
            return user

    @staticmethod
    async def cont_update_user_data(user_id: int, user_data: schemas.UsersUpdateDTO, auth_user_id: int):
        if user_id == auth_user_id:
            await AsyncORM.update_user_data(user_data)
            return True
        else:
            return False

    @staticmethod
    async def cont_update_user_password(user_id: int,
                                        new_password: str,
                                        old_password: str,
                                        auth_user_id: int,):
        if user_id == auth_user_id:
            async with async_session_factory() as session:
                user = await session.get(UsersModel, user_id)
                if user.password == Secure.sha256_str(old_password):
                    await AsyncORM.update_user_password(user_id, new_password)
                    return True

    @staticmethod
    async def cont_insert_channel(channel: schemas.ChannelsPostDTO, auth_user_id):
        if channel.owner_id == auth_user_id:
            async with async_session_factory() as session:
                query = (
                    select(ChannelsSubscriptionsModel)
                    .filter(ChannelsModel.short_name == channel.short_name)
                )
                alr_channel = await session.execute(query)
                if alr_channel.first() is None:
                    await AsyncORM.insert_channel(channel)
                    return True
        else:
            return False





