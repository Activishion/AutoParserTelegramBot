from sqlalchemy.ext.asyncio import AsyncSession

from services.logging_service import error_log, static_log
from settings.models import HistoryRequests


async def add_history_request(session: AsyncSession, data: dict[str, str]) -> None:
    obj_request = HistoryRequests(
        brand=data.get('brand'),
        model=data.get('model'),
        years=data.get('years'),
        mileage=data.get('mileage'),
        price=data.get('price'),
        user_id=data.get('user_id'),
        username=data.get('username'),
    )
    try:
        session.add(obj_request)
        static_log.info('Create request', **data)
        await session.commit()
    except Exception:
        error_log.error('Error request get_brand_and_model_auto')
