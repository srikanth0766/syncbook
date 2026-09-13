from sqlalchemy.orm import Session
from app.database.connection import engine, Base, SessionLocal
from app.models.channel import ChannelModel


def init_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        channels_data = [
            ("channel-a", "Channel A", "ONLINE"),
            ("channel-b", "Channel B", "ONLINE"),
            ("channel-c", "Channel C", "ONLINE"),
        ]
        for ch_id, ch_name, ch_status in channels_data:
            channel = db.query(ChannelModel).filter(ChannelModel.channel_id == ch_id).first()
            if not channel:
                channel = ChannelModel(channel_id=ch_id, name=ch_name, status=ch_status)
                db.add(channel)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
