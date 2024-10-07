import os
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base


class DBSettings(BaseSettings):
    DB_USERNAME: str = os.getenv('DB_USERNAME')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_DATABASE: str = os.getenv('DB_DATABASE')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')

    @property
    def data_source_name(self):
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"


db_settings = DBSettings()
engine = create_engine(db_settings.data_source_name, echo=False)
Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base(metadata=MetaData())
