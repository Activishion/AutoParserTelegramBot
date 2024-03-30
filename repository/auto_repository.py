from sqlalchemy import select, and_

from services.logging_service import error_log
from settings.database import async_session_maker
from settings.models import BrandModels


async def get_brand_and_model_auto(brand_name: str, model_name: str):
    async with async_session_maker() as session:
        stmt = (select(BrandModels.brand_id, BrandModels.model_id)
                .where(and_(
                    BrandModels.brand_name == brand_name,
                    BrandModels.model_name == model_name)
                ))
        try:
            result = await session.execute(stmt)
            return result.scalar()
        except Exception:
            error_log.error('Error request get_brand_and_model_auto')
