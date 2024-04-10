from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services import parsing_service
from settings.data.dict_marks import dict_marks_car
from settings.data.dict_models import dict_models
from repository import history_requests


user_router = Router()


@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Приветствую тебя! Я твой виртуальный помощник по подбору автомобилей!')


@user_router.message(or_f(Command('about'), (F.text.lower() == 'о нас')))
async def start_menu(message: types.Message):
    await message.answer('тут мы расскажем о нашем боте.')


class GetAuto(StatesGroup):
    brand = State()
    model = State()
    years = State()
    mileage = State()
    price = State()

    product_for_change = None

    texts = {
        'GetAuto:brand': 'Введите марку авто заново: ',
        'GetAuto:model': 'Введите модель заново: ',
        'GetAuto:years': 'Введите необходимые года заново: ',
        'GetAuto:mileage': 'Введите нужный пробег заново: ',
        'GetAuto:price': 'Этот стейт последний...'
    }


@user_router.message(StateFilter(None), or_f(Command('find_auto'), (F.text.lower() == 'найти авто')))
async def add_filters(message: types.Message, state: FSMContext):
    await message.answer('Введите марку авто')
    await state.set_state(GetAuto.brand)


@user_router.message(StateFilter("*"), Command("отмена"))
@user_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if GetAuto.product_for_change:
        GetAuto.product_for_change = None
    await state.clear()
    await message.answer("Действия отменены")


@user_router.message(StateFilter("*"), Command("назад"))
@user_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == GetAuto.brand:
        await message.answer('Предыдущего шага нет, напишите "отмена"')
        return

    previous = None
    for step in GetAuto.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {GetAuto.texts[previous.state]}")
            return
        previous = step


@user_router.message(GetAuto.brand, F.text)
async def add_brand(message: types.Message, state: FSMContext):
    if len(message.text) >= 50:
        await message.answer("Название марки авто не должно превышать 50 символов. \n Введите пожалуйста заново")
        return
    
    if dict_marks_car.get(message.text.lower(), None) is None:
        await message.answer('Введенная вами марка не найдена в списке допустимых')
        return

    await state.update_data(brand=message.text.lower())
    await message.answer('Введите модель авто')
    await state.set_state(GetAuto.model)


@user_router.message(GetAuto.model, F.text)
async def add_model(message: types.Message, state: FSMContext):
    if len(message.text) >= 50:
        await message.answer("Название модели авто не должно превышать 50 символов. \n Введите пожалуйста заново")
        return
    
    if dict_models.get(message.text.lower(), None) is None:
        await message.answer('Введенная вами модель не найдена в списке допустимых')
        return

    await state.update_data(model=message.text.lower())
    await message.answer('Введите необходимые годы выпуска авто в формате 2000-2020')
    await state.set_state(GetAuto.years)


@user_router.message(GetAuto.years, F.text)
async def add_years(message: types.Message, state: FSMContext):
    year_min = message.text.split('-')[0]
    year_max = message.text.split('-')[1]
    if len(year_min) > 4 or len(year_max) > 4 or int(year_min) > int(year_max):
        await message.answer("Вы указали необходимые года автомобиля не в том формате. \n Введите пожалуйста заново")
        return

    await state.update_data(years=message.text)
    await message.answer('Введите пробег авто в формате: "от-до"')
    await state.set_state(GetAuto.mileage)


@user_router.message(GetAuto.mileage, F.text)
async def add_mileage(message: types.Message, state: FSMContext):
    await state.update_data(mileage=message.text)
    await message.answer('Введите цену в формате: "от-до"')
    await state.set_state(GetAuto.price)


@user_router.message(GetAuto.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    price_min = message.text.split('-')[0]
    price_max = message.text.split('-')[1]

    if not price_min and not price_max:
        await message.answer("Вы не указали рассматриваемую сумму, или указали ее не в том формате. \n Введите пожалуйста заново")
        return
    await state.update_data(price=message.text)
 
    data = await state.get_data()
    data['user_id'] = message.from_user.id
    data['username'] = message.from_user.username
    text_message = (
         "Начинаю поиск по машине:\n"
        f"Марка: {data.get('brand')}\n"
        f"Модель: {data.get('model')}\n"
        f"Годы выпуска: {data.get('years')}\n"
        f"Пробег: {data.get('mileage')}\n"
        f"Цена: {data.get('price')}"
    )
    await message.answer(text_message)
    await history_requests.add_history_request(data=data)
    result_wallapop: list[str] = await parsing_service.get_content_wallapop(data=data)
    result_coches: list[str] = await parsing_service.get_content_coches(data=data)
    result = result_wallapop + result_coches

    if len(result) == 0:
        await message.answer('По вашему запросу ничего не найдено, попробуйте изменить критерии поиска')
    else:
        await message.answer(str('\n'.join(result)))
    await state.clear()
