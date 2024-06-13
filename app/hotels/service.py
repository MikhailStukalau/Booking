from datetime import date

from sqlalchemy import and_, or_, select, insert, func

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService
from app.database import engine, async_session_maker


class HotelService(BaseService):
    model = Hotels

    @classmethod
    async def find_all(
            cls,
            date_from: date,
            date_to: date,
            location: str
    ):

        """
        WITH booked_rooms AS (
                SELECT room_id, COUNT(room_id) AS rooms_booked
                FROM bookings
                WHERE
                    (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                    (date_from <= '2023-05-15' AND date_to > '2023-05-15')
                GROUP BY room_id
            ),
            booked_hotels AS (
                SELECT hotel_id, SUM(rooms.quantity - COALESCE(rooms_booked, 0)) AS rooms_left
                FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                GROUP BY hotel_id
            )
        SELECT * FROM hotels
        LEFT JOIN booked_hotels ON booked_hotels.hotel_id = hotels.id
        WHERE rooms_left > 0 AND location LIKE '%Алтай%';
        """
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                    and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
                )
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        booked_hotels = (
            select(Rooms.hotel_id, func.sum(Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)))
            .label("rooms_left")
            .select_from("Rooms")
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id)
            .cte("booked_hotels")
        )

        get_hotels_with_rooms = (
            select(Hotels.__table__.columns, booked_hotels.c.rooms_left)
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotels.location.like(f"%{location}%")
                )
            )
        )

        async with async_session_maker() as session:
            # logger.debug(get_hotels_with_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            print(get_hotels_with_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()