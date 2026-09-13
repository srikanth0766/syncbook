import os

class Settings:
    PROJECT_NAME: str = "Hotel PMS Service"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5431/hotel_db"
    )

settings = Settings()
