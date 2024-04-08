from datetime import datetime
from sqlalchemy import text

from settings.database import async_session_maker


async def add_history_request(data: dict[str, str]) -> None:
    async with async_session_maker() as session:
        stmt = text("""
            INSERT INTO history_requests(brand, model, years, mileage, price, date_request, user_id, username)
            VALUES (:brand, :model, :years, :mileage, :price, :date_request, :user_id, :username)
            """)
        await session.execute(stmt, {'brand': data.get('brand'), 'model': data.get('model'),
                                     'years': data.get('years'), 'mileage': data.get('mileage'),
                                     'price': data.get('price'), 'date_request': datetime.now(),
                                     'user_id': data.get('user_id'), 'username': data.get('username')})
        await session.commit()
