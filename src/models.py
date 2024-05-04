import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class ProductsModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    type: Mapped[Optional[str]] = mapped_column()
    price_rub: Mapped[Optional[float]] = mapped_column()
    status_active: Mapped[bool] = mapped_column(default=True)
    tags: Mapped[list["ProductsCatalogModel"]] = relationship(
        back_populates="product",
        primaryjoin="ProductsModel.id == ProductsCatalogModel.product_id"
    )
    feedbacks: Mapped[list["ProductsFeedbacksModel"]] = relationship(
        back_populates="product",
        primaryjoin="ProductsModel.id == ProductsFeedbacksModel.product_id"
    )


class ProductsCatalogModel(Base):
    __tablename__ = "products_catalog"

    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped["ProductsModel"] = relationship(
        back_populates="tags",
    )
    tag: Mapped["TagsModel"] = relationship(
        back_populates="products"
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))


class ProductsFeedbacksModel(Base):
    __tablename__ = "products_feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product: Mapped["ProductsModel"] = relationship(
        back_populates="feedbacks"
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    text: Mapped[str] = mapped_column()
    rating_up: Mapped[int] = mapped_column(default=0)
    rating_down: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime.datetime] = mapped_column()


class PurchasesModel(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    price_rub: Mapped[Optional[float]] = mapped_column()
    payment_type: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column()


class FilesModel(Base):
    __tablename__ = "files"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column()
    path: Mapped[Optional[str]] = mapped_column()


class UsersModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column()
    avatar_file_id: Mapped[Optional[str]] = mapped_column(ForeignKey("files.id"))
    reg_date: Mapped[datetime.datetime] = mapped_column()
    about: Mapped[Optional[str]] = mapped_column()
    quote: Mapped[Optional[str]] = mapped_column()
    favorite_writer: Mapped[Optional[str]] = mapped_column()
    favorite_book: Mapped[Optional[str]] = mapped_column()
    balance: Mapped[float] = mapped_column(default=0.0)

    bookshelf: Mapped["UsersBookcaseModel"] = relationship(
        back_populates="user",
        uselist=False
    )
    favourites_posts: Mapped[list["UsersFavouritesPostsModel"]] = relationship(
        back_populates="user"
    )
    favourites_tags: Mapped[list["UsersFavouritesTags"]] = relationship(
        back_populates="user"
    )
    library: Mapped[list["UsersLibrariesModel"]] = relationship(
        back_populates="user",
        uselist=False
    )
    wishlist: Mapped[list["UsersWishlistsModel"]] = relationship(
        back_populates="user",
        uselist=False
    )
    channels: Mapped[list["ChannelsModel"]] = relationship(
        back_populates="owner",
        primaryjoin="UsersModel.id == ChannelsModel.owner_id"
    )
    subscriptions: Mapped[list["ChannelsSubscriptionsModel"]] = relationship(
        back_populates="user",
    )
    group: Mapped["UsersGroupsModel"] = relationship(
        back_populates="user",
        uselist=False,
    )


class UsersBookcaseModel(Base):
    __tablename__ = "users_bookshelves"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["UsersModel"] = relationship(
        back_populates="bookshelf",
        uselist=False,
    )
    user_id: Mapped["int"] = mapped_column(ForeignKey("users.id"))
    first_book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    second_book_id: Mapped[Optional[int]] = mapped_column(ForeignKey("books.id"))
    third_book_id: Mapped[Optional[int]] = mapped_column(ForeignKey("books.id"))
    fourth_book_id: Mapped[Optional[int]] = mapped_column(ForeignKey("books.id"))
    fifth_book_id: Mapped[Optional[int]] = mapped_column(ForeignKey("books.id"))


class UsersFavouritesPostsModel(Base):
    __tablename__ = "users_favourites_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["UsersModel"] = relationship(
        back_populates="favourites_posts"
    )
    user_id: Mapped["int"] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped["int"] = mapped_column(ForeignKey("posts.id"))


class UsersFavouritesTags(Base):
    __tablename__ = "users_favourites_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["UsersModel"] = relationship(
        back_populates="favourites_tags"
    )
    tag: Mapped["TagsModel"] = relationship(
        back_populates="users"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tag_id: Mapped[str] = mapped_column(ForeignKey("tags.id"))
    tag_desc: Mapped[str] = mapped_column()


class UsersLibrariesModel(Base):
    __tablename__ = "users_libraries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["UsersModel"] = relationship(
        back_populates="library",
        uselist=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product_type: Mapped[str] = mapped_column()


class UsersWishlistsModel(Base):
    __tablename__ = "users_wish_list"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["UsersModel"] = relationship(
        back_populates="wishlist",
        uselist=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product_type: Mapped[str] = mapped_column()


class ChannelsModel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped["UsersModel"] = relationship(
        back_populates="channels",
        primaryjoin="ChannelsModel.owner_id == UsersModel.id"
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column()
    short_name: Mapped[Optional[str]] = mapped_column()
    about: Mapped[Optional[str]] = mapped_column()
    avatar_file_id: Mapped[Optional[str]] = mapped_column(ForeignKey("files.id"))
    total_subscription: Mapped[int] = mapped_column(default=0)
    reg_date: Mapped[datetime.datetime] = mapped_column()
    subscribers: Mapped[list["ChannelsSubscriptionsModel"]] = relationship(
        back_populates="channel"
    )
    posts: Mapped[list["PostsModel"]] = relationship(
        back_populates="channel"
    )


class ChannelsSubscriptionsModel(Base):
    __tablename__ = "channels_subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel: Mapped["ChannelsModel"] = relationship(
        back_populates="subscribers"
    )
    user: Mapped["UsersModel"] = relationship(
        back_populates="subscriptions",
    )
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class PostsModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    channel: Mapped["ChannelsModel"] = relationship(
        back_populates="posts"
    )
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"))
    title: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column()
    picture_file_id: Mapped[Optional[str]] = mapped_column(ForeignKey("files.id"))
    rating_up: Mapped[int] = mapped_column(default=0)
    rating_down: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime.datetime] = mapped_column()
    comments: Mapped[list["PostsCommentsModel"]] = relationship(
        back_populates="post"
    )


class PostsCommentsModel(Base):
    __tablename__ = "posts_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post: Mapped["PostsModel"] = relationship(
        back_populates="comments"
    )
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    parent_comment_id: Mapped[Optional[int]] = mapped_column()
    text: Mapped[str] = mapped_column()
    rating_up: Mapped[int] = mapped_column(default=0)
    rating_down: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime.datetime] = mapped_column()


class BooksModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("products.id"))
    name: Mapped[str] = mapped_column()
    desc: Mapped[Optional[str]] = mapped_column()
    author: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    format: Mapped[str] = mapped_column()
    file_id: Mapped[Optional[str]] = mapped_column(ForeignKey("files.id"))
    cover_file_id: Mapped[Optional[str]] = mapped_column(ForeignKey("files.id"))
    rating_up: Mapped[int] = mapped_column(default=0)
    rating_down: Mapped[int] = mapped_column(default=0)
    release_year: Mapped[Optional[int]] = mapped_column()
    publisher_alias: Mapped[Optional[str]] = mapped_column()
    publisher_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    publication_date: Mapped[datetime.datetime] = mapped_column()
    reviews: Mapped[list["BooksReviewsModel"]] = relationship(
        back_populates="book",
        order_by="BooksReviewsModel.id.asc()",
    )


class BooksReviewsModel(Base):
    __tablename__ = "books_reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    book: Mapped["BooksModel"] = relationship(
        back_populates="reviews"
    )
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    title: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column()
    estimation: Mapped[str] = mapped_column()
    rating_up: Mapped[int] = mapped_column(default=0)
    rating_down: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime.datetime] = mapped_column()


class TagsModel(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    products: Mapped[list["ProductsCatalogModel"]] = relationship(
        back_populates="tag"
    )
    users: Mapped[list["UsersFavouritesTags"]] = relationship(
        back_populates="tag"
    )


class UsersGroupsModel(Base):
    __tablename__ = "users_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    user: Mapped["UsersModel"] = relationship(
        back_populates="group",
        uselist=False,
    )
    group: Mapped["GroupsModel"] = relationship(
        back_populates="users"
    )


class GroupsModel(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    users: Mapped[list["UsersGroupsModel"]] = relationship(
        back_populates="group"
    )
    rules: Mapped[list["GroupsRulesModel"]] = relationship(
        back_populates="group"
    )


class GroupsRulesModel(Base):
    __tablename__ = "groups_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    rule_id: Mapped[int] = mapped_column(ForeignKey("rules.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["GroupsModel"] = relationship(
        back_populates="rules",
    )
    rule: Mapped["RulesModel"] = relationship(
        back_populates="groups"
    )


class RulesModel(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    groups: Mapped[list["GroupsRulesModel"]] = relationship(
        back_populates="rule"
    )

