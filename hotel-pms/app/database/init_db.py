from sqlalchemy.orm import Session
from app.database.connection import engine, Base, SessionLocal
from app.models.hotel import HotelModel
from app.models.room_type import RoomTypeModel


def init_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        hotel = db.query(HotelModel).filter(HotelModel.hotel_id == 1).first()
        if not hotel:
            hotel = HotelModel(hotel_id=1, name="Hotel A", location="New York")
            db.add(hotel)
            db.commit()

        room_types = [
            (1, "Standard Room", 10),
            (2, "Deluxe Room", 5),
            (3, "Suite", 2),
        ]
        for rt_id, rt_name, rt_total in room_types:
            rt = db.query(RoomTypeModel).filter(RoomTypeModel.room_type_id == rt_id).first()
            if not rt:
                rt = RoomTypeModel(room_type_id=rt_id, hotel_id=1, name=rt_name, total_rooms=rt_total)
                db.add(rt)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
