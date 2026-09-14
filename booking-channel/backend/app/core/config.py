import os

class Settings:
    PROJECT_NAME: str = "Booking Channel Service"
    CHANNEL_ID: str = os.getenv("CHANNEL_ID", "channel-a")
    CHANNEL_NAME: str = os.getenv("CHANNEL_NAME", "Channel A")
    QUEUE_NAME: str = os.getenv("QUEUE_NAME", "channel_a_queue")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5433/channel_a_db"
    )

settings = Settings()
