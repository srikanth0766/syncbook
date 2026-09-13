from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.hotel import HotelModel
from app.models.room_type import RoomTypeModel


def get_all_hotels(db: Session) -> List[HotelModel]:
    return db.query(HotelModel).all()


def get_hotel_by_id(db: Session, hotel_id: int) -> Optional[HotelModel]:
    return db.query(HotelModel).filter(HotelModel.hotel_id == hotel_id).first()


def get_room_types_by_hotel(db: Session, hotel_id: int) -> List[RoomTypeModel]:
    return db.query(RoomTypeModel).filter(RoomTypeModel.hotel_id == hotel_id).all()
