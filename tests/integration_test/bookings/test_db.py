from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=12, day=31),
        date_to=date(year=2025, month=1, day=1),
        price=100,
    )

    new_booking_data = await db.bookings.add(booking_data)
    print(f"{new_booking_data=}")

    # Получить это бронирование и убедиться, что она есть
    select_booking_data = await db.bookings.get_one_or_none(id=new_booking_data.id)
    print(f"{select_booking_data=}")

    assert (
        (booking_data.user_id == select_booking_data.user_id)
        & (booking_data.room_id == select_booking_data.room_id)
        & (booking_data.date_from == select_booking_data.date_from)
        & (booking_data.date_to == select_booking_data.date_to)
        & (booking_data.price == select_booking_data.price)
    )

    # Обновить бронирование (дату завершения)
    update_date_to = date(year=2025, month=1, day=10)
    update_price = 200
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=12, day=31),
        date_to=update_date_to,
        price=update_price,
    )

    await db.bookings.edit(update_booking_data, id=select_booking_data.id)
    updated_booking_data = await db.bookings.get_one_or_none(id=select_booking_data.id)
    print(f"{updated_booking_data=}")

    assert (
        (select_booking_data.id == updated_booking_data.id)
        & (booking_data.user_id == updated_booking_data.user_id)
        & (booking_data.room_id == updated_booking_data.room_id)
        & (booking_data.date_from == updated_booking_data.date_from)
        & (update_date_to == updated_booking_data.date_to)
        & (update_price == updated_booking_data.price)
    )

    # Удалить бронь
    await db.bookings.delete(id=updated_booking_data.id)
    booking = await db.bookings.get_one_or_none(id=select_booking_data.id)
    assert not booking

    await db.commit()
