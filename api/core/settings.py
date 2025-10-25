from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Country Currency & Exchange API"
    VERSION: str = "1.0.0"

    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "countrydb"

    COUNTRIES_API: str = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
    EXCHANGE_API: str = "https://open.er-api.com/v6/latest/USD"

    class Config:
        env_file = ".env"


settings = Settings()
