import os
from dotenv import load_dotenv


class Settings:
    load_dotenv()

    @staticmethod
    def database_url_psycopg():

        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_pass = os.getenv('DB_PASS')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')

        # postgresql+psycopg://user:password@host:port/dbname
        return f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    @staticmethod
    def database_url_asyncpg():

        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_pass = os.getenv('DB_PASS')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')

        # postgresql+asyncpg://user:password@host:port/dbname
        return f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    @staticmethod
    def file_storage_path():

        storage_path = os.getenv('STORAGE_PATH')
        return f"{storage_path}"

    @staticmethod
    def default_abc():

        default_abc = os.getenv('DF_ABC')
        return f"{default_abc}"
