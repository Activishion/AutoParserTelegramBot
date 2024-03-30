from aiogram.types import BotCommand


private = [
    BotCommand(command='about', description='О нас'),
    BotCommand(command='find_auto', description='Найти авто'),
]

admin = [
    BotCommand(command='statistics', description='Получить статистику за день')
]
