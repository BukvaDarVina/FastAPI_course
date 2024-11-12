from fastapi import Query, APIRouter, Body
from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "Dubai"},
]


@router.get("", summary="Получение списка всех отелей")
def get_hotels(
        id: int | None = Query(default=None, description="Айдишник отеля"),
        title: str | None = Query(default=None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Добавление отеля")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай 3 звезды у рынка",
        "name": "dubai_u_rinka",
    }},
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title and hotel_data.name:
                hotel["title"] = hotel_data.title
                hotel["name"] = hotel_data.name
                return hotel
    return {"status": "Error", "description": "Указаны не все параметры"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title and hotel_data.name:
                put_hotel(hotel_id=hotel_id, title=hotel_data.title, name=hotel_data.name)
            elif hotel_data.title:
                hotel["title"] = hotel_data.title
            elif hotel_data.name:
                hotel["name"] = hotel_data.name
            else:
                return {"status": "Error", "description": "Параметры не указаны"}
            return hotel
    return {"status": "Error", "description": "Параметры не указаны"}
