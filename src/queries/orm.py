import datetime
from sqlalchemy import text, insert, select, update, func, or_, update
from sqlalchemy.orm import selectinload, joinedload
from src.database import session_factory, async_session_factory
from src.secure import Secure
from src.models import *
from src import schemas


class SyncORM:

    @staticmethod
    def insert_new_user(user: schemas.UsersPostDTO):
        db_user = UsersModel(
            name=user.name,
            email=user.email,
            nickname=user.nickname,
            password=Secure.sha256_str(str(user.password)),
            reg_date=datetime.datetime.now(),
        )
        with session_factory() as session:
            session.add(db_user)
            session.commit()
            return True

    @staticmethod
    def insert_user_bookshelf(bookshelf: schemas.UsersBookshelfPostDTO):
        db_bookshelf = UsersBookcaseModel(
            user_id=bookshelf.user_id,
            first_book_id=bookshelf.first_book_id,
            second_book_id=bookshelf.second_book_id,
            third_book_id=bookshelf.third_book_id,
            fourth_book_id=bookshelf.fourth_book_id,
            fifth_book_id=bookshelf.fifth_book_id,
        )
        with session_factory() as session:
            session.add(db_bookshelf)
            session.commit()
            return db_bookshelf

    @staticmethod
    def update_user_bookshelf(user_id: int, update_bookshelf: schemas.UsersBookshelfUpdateDTO):
        with session_factory() as session:
            bookshelf = session.query(UsersBookcaseModel).filter_by(user_id=user_id).all()
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
            session.commit()

    @staticmethod
    def insert_user_favorite_post(post: schemas.UsersFavouritesPostsPostDTO):
        db_post = UsersFavouritesPostsModel(
            user_id=post.user_id,
            post_id=post.post_id,
        )
        with session_factory() as session:
            session.add(db_post)
            session.commit()
            return True

    @staticmethod
    def insert_user_favorite_tag(tag: schemas.UsersFavouritesTagsPostDTO):
        db_tag = UsersFavouritesTags(
            user_id=tag.user_id,
            tag_id=tag.tag_id,
            tag_desc=tag.tag_desc,
        )
        with session_factory() as session:
            session.add(db_tag)
            session.commit()
            return db_tag

    @staticmethod
    def insert_product_in_user_library(product: schemas.UsersLibrariesPostDTO):
        db_product = UsersLibrariesModel(
            user_id=product.user_id,
            product_id=product.product_id,
            product_type=product.product_type,
        )
        with session_factory() as session:
            session.add(db_product)
            session.commit()
            return True

    @staticmethod
    def insert_user_wish(wish: schemas.UsersWishlistsPostDTO):
        db_wish = UsersWishlistsModel(
            user_id=wish.user_id,
            product_id=wish.product_id,
            product_type=wish.product_type,
        )
        with session_factory() as session:
            session.add(db_wish)
            session.commit()
            return True

    @staticmethod
    def insert_user_subscription(subscription: schemas.ChannelsSubscriptionsPostDTO):
        db_sub = ChannelsSubscriptionsModel(
            user_id=subscription.user_id,
            channel_id=subscription.channel_id,
        )
        with session_factory() as session:
            session.add(db_sub)
            session.commit()
            return True

    @staticmethod
    def select_all_users(limit=100):
        with session_factory() as session:
            query = (
                select(UsersModel)
                .limit(limit)
            )
            res = session.execute(query)
            result = res.scalars().unique().all()
            return result

    @staticmethod
    def find_users(key_word):
        with session_factory() as session:
            query = (
                select(
                    UsersModel
                )
                .select_from(UsersModel)
                .filter(or_(UsersModel.name.contains(key_word),
                            UsersModel.nickname.contains(key_word),
                            ))
            )
            result = session.execute(query)
            return result.scalars().unique().all()

    @staticmethod
    def select_full_user(user_id):
        with session_factory() as session:
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
                .select_from(UsersModel)
                .filter(UsersModel.id == user_id)
            )
            result = session.execute(query)
            return result.scalars().unique().all()

    @staticmethod
    def update_user_fields(user_id: int,
                           column_name: str,
                           new_value):
        with session_factory() as session:
            user = session.query(UsersModel).filter_by(id=user_id).all()
            setattr(user, column_name, new_value)
            session.commit()

    @staticmethod
    def update_user_data(user_id: int, user_update: schemas.UsersUpdateDTO):
        with session_factory() as session:
            user = session.query(UsersModel).filter_by(id=user_id).all()
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
            session.commit()

    @staticmethod
    def update_user_password(user_id: int, new_password: str):
        new_password_hash = Secure.sha256_str(new_password)
        with session_factory() as session:
            user = session.query(UsersModel).filter_by(id=user_id).all()
            user.password = new_password_hash
            session.commit()

    @staticmethod
    def insert_channel():

        pass

    @staticmethod
    def select_all_channels(limit=100):
        with session_factory() as session:
            query = (
                select(ChannelsModel)
                .limit(limit)
            )
            res = session.execute(query)
            result = res.scalars().unique().all()
            return result

    @staticmethod
    def select_channel(channel_id):
        with session_factory() as session:
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
            result = session.execute(query)
            return result.scalars().unique().all()

    @staticmethod
    def update_channel_fields(channel_id: int,
                            column_name: str,
                            new_value):
        with session_factory() as session:
            channel = session.query(ChannelsModel).filter_by(id=channel_id).all()
            setattr(channel, column_name, new_value)
            session.commit()
            return True

    @staticmethod
    def insert_post():
        pass

    @staticmethod
    def select_all_posts(limit=100):
        with session_factory() as session:
            query = (
                select(PostsModel)
                .limit(limit)
            )
            res = session.execute(query)
            result = res.scalars().unique().all()
            return result

    @staticmethod
    def select_post(post_id):
        with session_factory() as session:
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
            result = session.execute(query)
            return result.scalars().unique().all()

    @staticmethod
    def update_post_data():
        pass

    @staticmethod
    def insert_comment():
        pass

    @staticmethod
    def select_all_post_comments(post_id):
        with session_factory() as session:
            query = (
                select(
                    PostsCommentsModel
                )
                .select_from(PostsCommentsModel)
                .filter(PostsCommentsModel.post_id == post_id)
            )
            result = session.execute(query)
            return result.scalars().unique().all()

    @staticmethod
    def select_comment(comment_id):
        with session_factory() as session:
            query = (
                select(
                    PostsCommentsModel
                )
                .options(selectinload(PostsCommentsModel.post))
                .select_from(PostsCommentsModel)
                .filter(PostsCommentsModel.id == comment_id)
            )
            result = session.execute(query)
            return result.scalars().unique().all()

    @staticmethod
    def delete_comment(comment_id):
        pass

    @staticmethod
    def select_file(file_id: str):
        with session_factory() as session:
            query = (
                select(
                    FilesModel
                )
                .select_from(FilesModel)
                .filter(FilesModel.id == file_id)
            )
            result = session.execute(query)
            return result.scalars().unique().all()

    @staticmethod
    def insert_file(file: schemas.FilesPostDTO):
        db_file = FilesModel(
            name=file.name,
            path=file.path,
            id=Secure.code_generator(None, 16)
        )
        with session_factory() as session:
            session.add(db_file)
            session.commit()

    @staticmethod
    def delete_file(file_id: str):
        with session_factory() as session:
            file = session.query(FilesModel).filter_by(id=file_id).first()
            session.delete(file)
            session.commit()

    @staticmethod
    def find_file(key_word: str):
        with session_factory() as session:
            query = (
                select(
                    FilesModel
                )
                .select_from(FilesModel)
                .filter(or_(FilesModel.name.contains(key_word),
                            FilesModel.id.contains(key_word),
                            ))
            )
            result = session.execute(query)
            return result.scalars().unique().all()


class ConvertDTO:

    @staticmethod
    def convert_to_dto(schema, obj):
        res_dto = [schema.model_validate(row, from_attributes=True) for row in obj]
        return res_dto


def let_it_happen():
    return
