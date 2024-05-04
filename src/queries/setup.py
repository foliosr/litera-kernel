from sqlalchemy import text, insert, func, cast, and_, select, Integer, inspect, or_
from sqlalchemy.orm import joinedload, selectinload
from src.secure import Secure
from src.database import sync_engine, async_engine, session_factory, async_session_factory, Base
from datetime import datetime
from src.models import *


class SetupDB:
    @staticmethod
    def create_table(table_name: str):
        Base.metadata.drop_all(sync_engine, tables=[Base.metadata.tables[table_name]])
        Base.metadata.create_all(sync_engine, tables=[Base.metadata.tables[table_name]])

    @staticmethod
    def create_all_tables():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

