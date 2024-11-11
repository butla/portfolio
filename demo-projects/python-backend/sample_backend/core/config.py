import enum
from typing import Final

from pydantic_settings import BaseSettings
import sqlalchemy


@enum.unique
class SSLMode(enum.StrEnum):
    require = enum.auto()
    prefer = enum.auto()


class AppConfig(BaseSettings):
    """Settings for the application. Taken from environment variables."""

    app_name: str = "Sample Python backend"

    postgres_host: str = "localhost"
    postgres_password: str = "postgres"
    postgres_database: str = "postgres"
    postgres_user: str = "postgres"
    postgres_port: int = 5432
    postgres_ssl_mode: SSLMode = SSLMode.prefer

    @property
    def postgres_url(self) -> sqlalchemy.URL:
        return sqlalchemy.URL.create(
            drivername="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_database,
            query={"sslmode": self.postgres_ssl_mode},
        )


SETTINGS: Final = AppConfig()
