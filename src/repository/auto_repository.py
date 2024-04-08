from sqlalchemy import text

from services.logging_service import error_log
from settings.database import async_session_maker


async def get_model_id_auto(model_name: str):
    async with async_session_maker() as session:
        stmt = text("""SELECT id FROM models WHERE model_name = :model_name""")
        try:
            result = await session.execute(stmt, {'model_name': model_name})
            return result.scalar_one_or_none()
        except Exception:
            error_log.error('Error request get_model_id_auto')
