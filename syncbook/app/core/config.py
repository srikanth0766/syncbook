import os

class Settings:
    PROJECT_NAME: str = "Syncbook CRS Service"
    INSTANCE_ID: str = os.getenv("INSTANCE_ID", "syncbook-1")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/syncbook_db"
    )

settings = Settings()
