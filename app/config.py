from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field


# base settings model
class SettingsBase(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra="ignore")


# database settings model
class DatabaseSettings(SettingsBase):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")


    # database connection string
    @computed_field
    @property
    def connection_string(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


# jwt settings
class JWTSettings(SettingsBase):
    key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")


# general entry point
class Settings(SettingsBase):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)


settings = Settings()