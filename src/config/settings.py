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
    MODEL_PATH: Path = BASE_PATH / "models"

    # LLM SETTINGS
    LLM_MODEL_FILE_NAME: str = "Meta-Llama-3.1-8B-Instruct-Q3_K_S.gguf"
    LLM_TOP_K: int = 50
    LLM_TOP_P: float = 0.9
    LLM_TEMPERATURE: float = 0.8
    LLM_N_THREADS: int = 3  # no.of cores - 1
    LLM_MAX_TOKENS: int = 2000
    LLM_N_CTX: int = 2048

    class Config:
        env_file = ".env"


settings = Settings()  # pyright: ignore
