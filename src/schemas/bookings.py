from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class BookingsAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookingPatch(BaseModel):
    date_from: date
    date_to: date
    price: int
