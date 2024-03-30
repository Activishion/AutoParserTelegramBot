import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class BotConfig:
    TOKEN: str = os.getenv('TELEGRAM_TOKEN')
    ADMINS_LIST: str = [1192371001]

    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT: int = os.getenv('POSTGRES_PORT')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')

    LOG_FORMAT: str = '%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    LOG_DATE_FORMAT: str = "%m/%d/%Y %H:%M:%S"

    @property
    def database_url_postgresql(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = BotConfig()
