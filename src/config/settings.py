from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DBNAME: str
    DBUSER: str
    DBPASSWORD: str
    DBHOST: str = "localhost"
    DBPORT: str = "5432"

    @property
    def POSTFRESQL_URI(self) -> str:
        return f"postgresql://{self.DBUSER}:{self.DBPASSWORD}@{self.DBHOST}:{self.DBPORT}/{self.DBNAME}"

    BASE_PATH: Path = Path(__name__).resolve().parent

    class Config:
        env_file = ".env"


settings = Settings()  # pyright: ignore
