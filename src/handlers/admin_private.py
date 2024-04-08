from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command

from common.filters import IsAdmin


admin_router = Router()
admin_router.message.filter(IsAdmin())


@admin_router.message(Command('statistics'))
async def get_statistic_per_day(message: types.Message):
    await message.answer('Статистика за сутки')