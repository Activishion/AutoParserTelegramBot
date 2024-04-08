import asyncio

from aiogram import Dispatcher, types, Bot
from datetime import datetime

from common.bot_commands_list import private, admin
from handlers.admin_private import admin_router
from handlers.user_private import user_router
from services.logging_service import static_log
from settings.config import settings


bot = Bot(token=settings.TOKEN)

dp = Dispatcher()
dp.include_router(admin_router)
dp.include_router(user_router)


async def on_startup(bot) -> None:
    static_log.info('Bot started')
    print('Bot started', datetime.now())


async def on_shutdown(bot) -> None:
    static_log.info('Bot crash')
    print('Bot crash', datetime.now())


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=['message', 'edited_message'])
    

if __name__ == '__main__':
    asyncio.run(main())
