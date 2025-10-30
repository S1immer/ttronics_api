from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field(...)

    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=False)

    MAX_BATTERIES_PER_DEVICE: int = Field(default=5)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()  # type: ignore[call-arg]

# # type: ignore[call-arg] — это подсказка для IDE, что мы осознанно игнорируем предупреждение,
# связанное с непереданными параметрами.
# При этом на выполнение программы это не влияет — Pydantic всё равно подтянет переменные из .env во время запуска.
