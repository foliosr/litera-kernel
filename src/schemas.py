from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UsersPostDTO(BaseModel):
    name: str
    email: str
    nickname: str
    password: str


class UsersDTO(UsersPostDTO):
    id: int
    avatar_file_id: Optional[str]
    reg_date: datetime
    about: Optional[str]
    quote: Optional[str]
    favorite_writer: Optional[str]
    favorite_book: Optional[str]
    balance: float


class UsersRelDTO(UsersDTO):
    bookshelf: Optional["UsersBookshelfDTO"]
    favourites_posts: Optional[list["UsersFavouritesPostsDTO"]]
    favourites_tags: Optional[list["UsersFavouritesTagsDTO"]]
    library: Optional[list["UsersLibrariesDTO"]]
    wishlist: Optional[list["UsersWishlistsDTO"]]
    channels: Optional[list["ChannelsDTO"]]
    subscriptions: Optional[list["ChannelsSubscriptionsDTO"]]
    group: "UsersGroupsDTO"


class UsersShortDTO(BaseModel):
    id: int
    name: str
    nickname: str
    avatar_file_id: Optional[str]
    about: Optional[str]
    quote: Optional[str]
    favorite_writer: Optional[str]
    favorite_book: Optional[str]


class UsersUpdateDTO(BaseModel):
    name: Optional[str]
    email: Optional[str]
    avatar_file_id: Optional[str]
    about: Optional[str]
    quote: Optional[str]
    favorite_writer: Optional[str]
    favorite_book: Optional[str]


class UsersShortRelDTO(UsersShortDTO):
    bookshelf: Optional["UsersBookshelfDTO"]
    favourites_tags: Optional[list["UsersFavouritesTagsDTO"]]


class UsersBookshelfPostDTO(BaseModel):
    user_id: int
    first_book_id: int
    second_book_id: Optional[int]
    third_book_id: Optional[int]
    fourth_book_id: Optional[int]
    fifth_book_id: Optional[int]


class UsersBookshelfDTO(UsersBookshelfPostDTO):
    id: int


class UsersBookshelfUpdateDTO(BaseModel):
    first_book_id: Optional[int]
    second_book_id: Optional[int]
    third_book_id: Optional[int]
    fourth_book_id: Optional[int]
    fifth_book_id: Optional[int]


class UsersFavouritesPostsPostDTO(BaseModel):
    user_id: int
    post_id: int


class UsersFavouritesPostsDTO(UsersFavouritesPostsPostDTO):
    id: int


class UsersLibrariesPostDTO(BaseModel):
    user_id: int
    product_id: int
    product_type: str


class UsersLibrariesDTO(UsersLibrariesPostDTO):
    id: int


class UsersWishlistsPostDTO(BaseModel):
    user_id: int
    product_id: int
    product_type: str


class UsersWishlistsDTO(UsersWishlistsPostDTO):
    id: int


class UsersFavouritesTagsPostDTO(BaseModel):
    user_id: int
    tag_id: str
    tag_desc: str


class UsersFavouritesTagsDTO(UsersFavouritesTagsPostDTO):
    id: int


class UsersFavouritesTagsRelDTO(UsersFavouritesTagsPostDTO):
    user: "UsersShortDTO"
    tag: "TagsDTO"


class ChannelsPostDTO(BaseModel):
    owner_id: int
    name: int
    short_name: Optional[str]


class ChannelsUpdateDTO(BaseModel):
    name: Optional[int]
    about: Optional[str]
    avatar_file_id: Optional[str]


class ChannelsDTO(ChannelsPostDTO):
    id: int
    about: Optional[str]
    avatar_file_id: Optional[str]
    total_subscription: int


class ChannelsRelDTO(ChannelsDTO):
    owner: "UsersShortDTO"
    subscribers: Optional[list["ChannelsSubscriptionsDTO"]]
    posts: Optional[list["PostsDTO"]]


class PostsPostDTO(BaseModel):
    user_id: int
    channel_id: int
    title: str
    body: str
    picture_file_id: Optional[str]


class PostsDTO(PostsPostDTO):
    id: int
    rating_up: int
    rating_down: int
    created_at: datetime


class PostsRelDTO(PostsDTO):
    channel: "ChannelsDTO"
    comments: Optional[list["PostsCommentsDTO"]]


class PostsCommentsPostDTO(BaseModel):
    user_id: int
    post_id: int
    parent_comment_id: Optional[int]
    text: str


class PostsCommentsDTO(PostsCommentsPostDTO):
    id: int
    rating_up: int
    rating_down: int
    created_at: datetime


class PostsCommentsRelDTO(PostsCommentsDTO):
    post: "PostsDTO"


class ProductsPostDTO(BaseModel):
    name: str
    type: str
    price_rub: float


class ProductsDTO(ProductsPostDTO):
    id: int
    status_active: bool


class ProductsRelDTO(ProductsDTO):
    tags: list["ProductsCatalogDTO"]
    feedbacks: list["ProductsFeedbacksDTO"]


class ProductsCatalogPostDTO(BaseModel):
    product_id: int
    catalog_tag: int


class ProductsCatalogDTO(ProductsCatalogPostDTO):
    id: int


class ProductsCatalogRelDTO(ProductsCatalogDTO):
    product: "ProductsCatalogDTO"
    tag: "TagsDTO"


class ProductsFeedbacksPostDTO(BaseModel):
    user_id: int
    product_id: int
    text: str


class ProductsFeedbacksDTO(ProductsFeedbacksPostDTO):
    id: int
    rating_up: int
    rating_down: int
    created_at: datetime


class TagsPostDTO(BaseModel):
    name: str


class TagsDTO(TagsPostDTO):
    id: int


class TagsRelDTO(TagsPostDTO):
    products: list["ProductsDTO"]


class BooksPostDTO(BaseModel):
    name: str
    desc: Optional[str]
    product_id: Optional[int]
    file_id: Optional[str]
    cover_file_id: Optional[str]
    author: str
    type: str
    format: str
    release_year: Optional[str]
    publisher_alias: Optional[str]
    publisher_user_id: Optional[int]


class BooksDTO(BooksPostDTO):
    id: int
    rating_up: int
    rating_down: int
    publication_date: datetime


class BooksRelDTO(BooksDTO):
    reviews: "BooksReviewsDTO"


class BooksPostReviewsDTO(BaseModel):
    book_id: int
    title: str
    body: str
    estimation: Optional[str]


class BooksReviewsDTO(BooksPostReviewsDTO):
    id: str
    rating_up: int
    rating_down: int
    created_at: datetime


class RulesPostDTO(BaseModel):
    name: str


class RulesDTO(RulesPostDTO):
    id: int


class RulesRelDTO(RulesDTO):
    groups: list["UsersGroupsDTO"]


class UsersGroupsPostDTO(BaseModel):
    name: str
    user_id: int
    group_id: int


class UsersGroupsDTO(UsersGroupsPostDTO):
    id: int


class UsersGroupsRelDTO(UsersGroupsDTO):
    user: "UsersShortDTO"
    group: "GroupsDTO"


class GroupsPostDTO(BaseModel):
    name: str


class GroupsDTO(GroupsPostDTO):
    id: int


class GroupsRulesPostDTO(BaseModel):
    rule_id: int
    group_id: int


class UsersGroupsRulesDTO(GroupsRulesPostDTO):
    id: int


class UsersGroupsRulesRelDTO(UsersGroupsRulesDTO):
    group: "UsersGroupsDTO"
    rule: "RulesDTO"


class ChannelsSubscriptionsPostDTO(BaseModel):
    user_id: int
    channel_id: int


class ChannelsSubscriptionsDTO(ChannelsSubscriptionsPostDTO):
    id: int
    created_at: datetime


class UsersSubscriptionsRelDTO(ChannelsSubscriptionsDTO):
    channel: "ChannelsDTO"
    user: "UsersShortDTO"


class FilesPostDTO(BaseModel):
    name: str
    path: str


class FilesDTO(FilesPostDTO):
    id: str


class FilesUpdateDTO(BaseModel):
    name: Optional[str]
    path: Optional[str]
