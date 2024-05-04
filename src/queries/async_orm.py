import datetime
from sqlalchemy import text, insert, select, update, func, or_, and_
from sqlalchemy.orm import selectinload, joinedload
from src.database import session_factory, async_session_factory
from src.secure import Secure
from src.models import *
from src import schemas


class AsyncORM:
    @staticmethod
    async def insert_new_user(user):
        db_user = UsersModel(
            name=user.name,
            email=user.email,
            nickname=user.nickname,
            password=Secure.sha256_str(str(user.password)),
            reg_date=datetime.datetime.now()
        )
        async with async_session_factory() as session:
            session.add(db_user)
            await session.commit()

    @staticmethod
    async def insert_user_bookshelf(bookshelf: schemas.UsersBookshelfPostDTO):
        db_bookshelf = UsersBookcaseModel(
            user_id=bookshelf.user_id,
            first_book_id=bookshelf.first_book_id,
            second_book_id=bookshelf.second_book_id,
            third_book_id=bookshelf.third_book_id,
            fourth_book_id=bookshelf.fourth_book_id,
            fifth_book_id=bookshelf.fifth_book_id,
        )
        async with async_session_factory() as session:
            session.add(db_bookshelf)
            await session.commit()

    @staticmethod
    async def update_user_bookshelf(user_id: int, update_bookshelf: schemas.UsersBookshelfUpdateDTO):
        query = (
            select(UsersBookcaseModel)
            .filter(UsersBookcaseModel.user_id == update_bookshelf.user_id)
            .select_from(UsersBookcaseModel)
        )
        async with async_session_factory() as session:
            bookshelf = session.execute(query).first()
            if update_bookshelf.first_book_id is not None:
                bookshelf.first_book_id = update_bookshelf.first_book_id
            if update_bookshelf.second_book_id is not None:
                bookshelf.second_book_id = update_bookshelf.second_book_id
            if update_bookshelf.third_book_id is not None:
                bookshelf.third_book_id = update_bookshelf.third_book_id
            if update_bookshelf.fourth_book_id is not None:
                bookshelf.fourth_book_id = update_bookshelf.fourth_book_id
            if update_bookshelf.fifth_book_id is not None:
                bookshelf.fifth_book_id = update_bookshelf.fifth_book_id

            await session.refresh(bookshelf)
            await session.commit()

    @staticmethod
    async def insert_user_favorite_post(post: schemas.UsersFavouritesPostsPostDTO):
        db_post = UsersFavouritesPostsModel(
            user_id=post.user_id,
            post_id=post.post_id,
        )
        async with async_session_factory() as session:
            session.add(db_post)
            await session.commit()

    @staticmethod
    async def delete_user_favorite_post(user_id: int, post_id: int):
        async with async_session_factory() as session:
            fav_post = await session.query(UsersFavouritesPostsModel).filter(
                and_(UsersFavouritesPostsModel.user_id == user_id,
                     UsersFavouritesPostsModel.post_id == post_id)).first()
            session.delete(fav_post)
            await session.commit()

    @staticmethod
    async def insert_user_favorite_tag(tag: schemas.UsersFavouritesTagsPostDTO):
        db_tag = UsersFavouritesTags(
            user_id=tag.user_id,
            tag_id=tag.tag_id,
            tag_desc=tag.tag_desc,
        )
        async with async_session_factory() as session:
            session.add(db_tag)
            await session.commit()

    @staticmethod
    async def delete_user_favorite_tag(user_id: int, tag_id: int):
        async with async_session_factory() as session:
            fav_tag = await session.query(UsersFavouritesTags).filter(
                and_(UsersFavouritesTags.user_id == user_id,
                     UsersFavouritesTags.tag_id == tag_id)).first()
            session.delete(fav_tag)
            await session.commit()

    @staticmethod
    async def insert_product_in_user_library(product: schemas.UsersLibrariesPostDTO):
        db_product = UsersLibrariesModel(
            user_id=product.user_id,
            product_id=product.product_id,
            product_type=product.product_type,
        )
        async with async_session_factory() as session:
            session.add(db_product)
            await session.commit()

    @staticmethod
    async def insert_user_wish(wish: schemas.UsersWishlistsPostDTO):
        db_wish = UsersWishlistsModel(
            user_id=wish.user_id,
            product_id=wish.product_id,
            product_type=wish.product_type,
        )
        async with async_session_factory() as session:
            session.add(db_wish)
            await session.commit()

    @staticmethod
    async def delete_user_wish(user_id: int, product_id: int):
        async with async_session_factory() as session:
            wish = await session.query(UsersWishlistsModel).filter(
                    and_(UsersWishlistsModel.user_id == user_id,
                         UsersWishlistsModel.product_id == product_id)).first()
            session.delete(wish)
            await session.commit()

    @staticmethod
    async def insert_user_subscription(subscription: schemas.ChannelsSubscriptionsPostDTO):
        db_sub = ChannelsSubscriptionsModel(
            user_id=subscription.user_id,
            channel_id=subscription.channel_id,
        )
        async with async_session_factory() as session:
            session.add(db_sub)
            await session.commit()

    @staticmethod
    async def delete_user_subscription(user_id: int, channel_id: int):
        async with async_session_factory() as session:
            sub = await session.query(ChannelsSubscriptionsModel).filter(
                and_(ChannelsSubscriptionsModel.user_id == user_id,
                     ChannelsSubscriptionsModel.channel_id == channel_id)).first()
            session.delete(sub)
            await session.commit()

    @staticmethod
    async def select_all_users(limit: int):
        async with async_session_factory() as session:
            query = (
                select(UsersModel)
                .limit(limit)
            )
            res = await session.execute(query)
            result = res.scalars().unique().all()
            return result

    @staticmethod
    async def find_users(key_word):
        async with async_session_factory() as session:
            query = (
                select(
                    UsersModel
                )
                .select_from(UsersModel)
                .filter(or_(UsersModel.name.contains(key_word),
                            UsersModel.nickname.contains(key_word),
                            ))
            )
            result = await session.execute(query)
            return result.scalars().unique().all()

    @staticmethod
    async def select_full_user(user_id):
        async with async_session_factory() as session:
            query = (
                select(
                    UsersModel
                )
                .options(selectinload(UsersModel.bookshelf),
                         selectinload(UsersModel.favourites_posts),
                         selectinload(UsersModel.favourites_tags),
                         selectinload(UsersModel.library),
                         selectinload(UsersModel.wishlist),
                         selectinload(UsersModel.channels),
                         selectinload(UsersModel.subscriptions)
                         )
                .filter(UsersModel.id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def update_user_fields(user_id: int,
                                 column_name: str,
                                 new_value):
        async with async_session_factory() as session:
            user = await session.query(UsersModel).filter_by(id=user_id).first()
            setattr(user, column_name, new_value)
            await session.commit()

    @staticmethod
    async def update_user_data(user_id: int, user_update: schemas.UsersUpdateDTO):
        async with async_session_factory() as session:
            query = (
                select(UsersModel)
                .filter(UsersModel.id == user_id)
            )
            res = await session.execute(query)
            user = res.first()
            if user_update.name is not None:
                user.name = user_update.name
            if user_update.email is not None:
                user.email = user_update.email
            if user_update.avatar_file_id is not None:
                user.avatar_file_id = user_update.avatar_file_id
            if user_update.about is not None:
                user.about = user_update.about
            if user_update.quote is not None:
                user.quote = user_update.quote
            if user_update.favorite_writer is not None:
                user.favorite_writer = user_update.favorite_writer
            if user_update.favorite_book is not None:
                user.favorite_book = user_update.favorite_book

            await session.commit(user)

    @staticmethod
    async def update_user_password(user_id: int, new_password: str):
        new_password_hash = Secure.sha256_str(new_password)
        async with async_session_factory() as session:
            user = await session.get(UsersModel, user_id)
            user.password = new_password_hash
            await session.commit()

    @staticmethod
    async def insert_channel(channel: schemas.ChannelsPostDTO):
        db_channel = UsersModel(
            owner_id=channel.owner_id,
            name=channel.name,
            short_name=channel.short_name,
        )
        async with async_session_factory() as session:
            session.add(db_channel)
            await session.commit()

    @staticmethod
    async def update_channel_data(channel_id: int, update_channel: schemas.ChannelsUpdateDTO):
        async with async_session_factory() as session:
            channel = session.query(ChannelsModel).filter_by(id=channel_id).first()
            if update_channel.name is not None:
                channel.name = update_channel.name
            if update_channel.path is not None:
                channel.about = update_channel.about
            if update_channel.path is not None:
                channel.avatar_file_id = update_channel.avatar_file_id

            session.merge(channel)
            await session.commit()

    @staticmethod
    async def select_all_channels(limit=100):
        async with async_session_factory() as session:
            query = (
                select(ChannelsModel)
                .limit(limit)
            )
            res = await session.execute(query)
            result = res.scalars().unique().all()
            return result

    @staticmethod
    async def select_channel(channel_id):
        async with async_session_factory() as session:
            query = (
                select(
                    ChannelsModel
                )
                .options(selectinload(ChannelsModel.owner),
                         selectinload(ChannelsModel.posts),
                         )
                .select_from(ChannelsModel)
                .filter(ChannelsModel.id == channel_id)
            )
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def update_channel_fields(channel_id: int,
                                    column_name: str,
                                    new_value):
        async with async_session_factory() as session:
            channel = await session.get(ChannelsModel, channel_id)
            setattr(channel, column_name, new_value)
            await session.commit()

    @staticmethod
    async def insert_post(post: schemas.PostsPostDTO):
        db_post = PostsModel(
            user_id=post.user_id,
            channel_id=post.channel_id,
            title=post.title,
            body=post.body,
            picture_file_id=post.picture_file_id,
        )
        async with async_session_factory() as session:
            session.add(db_post)
            await session.commit(db_post)

    @staticmethod
    async def select_all_posts(limit=100):
        async with async_session_factory() as session:
            query = (
                select(PostsModel)
                .limit(limit)
            )
            res = await session.execute(query)
            result = res.scalars().unique().all()
            return result

    @staticmethod
    async def select_post(post_id):
        async with async_session_factory() as session:
            query = (
                select(
                    PostsModel
                )
                .options(selectinload(PostsModel.channel),
                         selectinload(PostsModel.comments),
                         )
                .select_from(PostsModel)
                .filter(PostsModel.id == post_id)
            )
            result = await session.execute(query)
            return result.scalars().unique().all()

    @staticmethod
    async def find_product(key_word):
        async with async_session_factory() as session:
            query = (
                select(
                    UsersModel.id
                )
                .options(selectinload(BooksModel.reviews))
                .select_from(BooksModel)
                .filter(or_(UsersModel.name.contains(key_word),
                            BooksModel.author.contains(key_word),
                            ))
            )
            res = await session.execute(query)
            result = res.scalars().first()
            return result

    @staticmethod
    async def find_book_for_product(product_id: str):

        async with async_session_factory() as session:
            session.get()

    @staticmethod
    async def select_user(user_id):
        async with async_session_factory() as session:
            query = (
                select(UsersModel)
                .options(selectinload(UsersModel.bookshelf),
                         selectinload(UsersModel.favourites_posts),
                         selectinload(UsersModel.library),
                         selectinload(UsersModel.wishlist))
                .filter(UsersModel.id == user_id)
            )
            res = await session.execute(query)
            user = res.scalars().all()
            return user

    @staticmethod
    async def insert_book(book: schemas.BooksPostDTO):
        db_book = BooksModel(
            product_id=book.product_id,
            name=book.name,
            desc=book.desc,
            author=book.author,
            type=book.type,
            format=book.format,
            file_id=book.file_id,
            cover_file_id=book.cover_file_id,
            release_year=book.release_year,
            publisher_alias=book.publisher_alias,
            publisher_user_id=book.publisher_user_id,
            publication_date=datetime.datetime.now()
        )
        async with async_session_factory() as session:
            session.add(db_book)
            await session.commit()

    @staticmethod
    async def update_book_fields(book_id: int,
                                 column_name: str,
                                 new_value):
        async with async_session_factory() as session:
            book = await session.get(UsersModel, book_id)
            setattr(book.first(), column_name, new_value)
            await session.commit()

    @staticmethod
    async def select_all_books(limit=100):
        async with async_session_factory() as session:
            query = (
                select(BooksModel)
                .limit(limit)
            )
            res = await session.execute(query)
            result = res.scalars().unique().all()
            return result

    @staticmethod
    async def find_books(key_word):
        async with async_session_factory() as session:
            query = (
                select(
                    BooksModel
                )
                .options(selectinload(BooksModel.reviews))
                .select_from(BooksModel)
                .filter(or_(BooksModel.name.contains(key_word),
                            BooksModel.author.contains(key_word),
                            ))
            )
            res = await session.execute(query)
            result = res.scalars().all()
            return result

    @staticmethod
    async def select_book(book_id: int):
        async with async_session_factory as session:
            query = (
                select(BooksModel)
                .options(selectinload(BooksModel.reviews))
                .filter(BooksModel.id == book_id)
            )
            book = await session.execute(query)
            return book.first()

    @staticmethod
    async def insert_file(file: schemas.FilesPostDTO):
        db_file = FilesModel(
            name=file.name,
            path=file.path,
            id=Secure.code_generator(None, 16)
        )
        async with async_session_factory() as session:
            session.add(db_file)
            await session.commit()

    @staticmethod
    async def select_file(file_id: str):
        async with async_session_factory() as session:
            query = (
                select(
                    FilesModel
                )
                .select_from(FilesModel)
                .filter(FilesModel.id == file_id)
            )
            result = await session.execute(query)
            return result.first()

    @staticmethod
    async def update_file(file_id: str, update_file: schemas.FilesUpdateDTO):
        async with async_session_factory() as session:
            file = session.get(FilesModel, file_id)
            if update_file.name is not None:
                file.name = update_file.name
            if update_file.path is not None:
                file.path = update_file.path

            session.merge(file)
            await session.commit()

    @staticmethod
    async def delete_file(file_id: str):
        async with async_session_factory() as session:
            file = await session.get(FilesModel, file_id)
            session.delete(file)
            await session.commit()

    @staticmethod
    async def find_file(key_word: str):
        async with async_session_factory() as session:
            query = (
                select(
                    FilesModel
                )
                .select_from(FilesModel)
                .filter(or_(FilesModel.name.contains(key_word),
                            FilesModel.id.contains(key_word),
                            ))
            )
            result = await session.execute(query)
            return result.scalars().unique().all()

