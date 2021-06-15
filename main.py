from aiogram import Bot, Dispatcher, executor, types

from common.db_command import start_session
from common.bot_command import get_parent_categorys, check_category, get_category, check_show_products, get_products, \
    get_product, check_show_product, get_image, update_last_state, get_last_state, update_user_phone, create_user_state, \
    check_user_data, update_user_name, get_user_answer, update_last_product

from common.check_data import check_phone, check_name
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
LAST_STATE = 'start'

commands = {'about_company': {
        'father': 'start',
        'name': 'Узнать о бизнесе',
        'text': 'тут о бизнесе',
        'commands': ['my_story', '6_min', 'plan'],
    },
    'my_story': {
        'father': 'about_company',
        'name': 'Моя история',
        'text': 'тут очевидно твоя история',
        'commands': ['want_in_command'],
    },
    '6_min': {
        'father': 'about_company',
        'name': 'Коротко за 6 минут',
        'text': '6 минут',
        'commands': ['want_in_command'],
    },
    'plan': {
        'father': 'about_company',
        'name': 'Маркетинг план',
        'text': 'План',
        'commands': ['want_in_command'],
    },
}


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    create_user_state(session, message['from']['id'])
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.InlineKeyboardButton(text='Узнать о бизнесе', callback_data='about_company'))
    poll_keyboard.add(types.InlineKeyboardButton(text='Каталог товаров', callback_data='catalog'))
    await message.reply("хай", reply_markup=poll_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'start')
async def main_menu(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    update_last_state(session, user_id)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.InlineKeyboardButton(text='Узнать о бизнесе', callback_data='about_company'))
    poll_keyboard.add(types.InlineKeyboardButton(text='Каталог товаров', callback_data='catalog'))
    await bot.send_message(chat_id=user_id, text="Главное меню", reply_markup=poll_keyboard)


@dp.message_handler(lambda message: check_phone(message.text))
async def get_phone_command(message: types.Message):
    user = message['from']['id']
    update_user_phone(session, user, message.text)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if check_user_data(session, user):
        await bot.send_message(chat_id=user, text=get_user_answer(session, user), reply_markup=poll_keyboard)
    else:
        await bot.send_message(chat_id=user, text="Введите свое имя", reply_markup=poll_keyboard)


@dp.message_handler(lambda message: check_name(message.text))
async def get_name_command(message: types.Message):
    user = message['from']['id']
    update_user_name(session, user, message.text)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if check_user_data(session, user):
        await bot.send_message(chat_id=user, text=get_user_answer(session, user), reply_markup=poll_keyboard)
    else:
        await bot.send_message(chat_id=user, text="Введите номер телефона", reply_markup=poll_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'want_in_command')
async def want_in_command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    update_last_state(session, user_id)
    update_last_product(session, user_id, 'want_in_command')
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if check_user_data(session, user_id):
        await bot.send_message(chat_id=user_id, text=get_user_answer(session, user_id), reply_markup=poll_keyboard)
    else:
        await bot.send_message(chat_id=user_id, text=f"Введите номер своего телефона для связи",
                               reply_markup=poll_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data in commands)
async def command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    text = callback_query.data
    update_last_state(session, user_id, new_state=text)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for com in commands[text]['commands']:
        if com in commands:
            poll_keyboard.add(types.InlineKeyboardButton(text=commands[com]['name'], callback_data=f'{com}'))
        elif com == 'want_in_command':
            poll_keyboard.add(types.InlineKeyboardButton(text='Хочу в команду', callback_data=f'{com}'))
    if commands[text].get('father', None):
        poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"{get_last_state(session,user_id)}"))
    await bot.send_message(chat_id=user_id, text=f"{text}", reply_markup=poll_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'catalog')
async def catalog_command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    update_last_state(session, user_id, new_state=callback_query.data)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    categories = get_parent_categorys(session)
    for cat in categories:
        poll_keyboard.add(types.InlineKeyboardButton(text=cat.name, callback_data=f'{cat.command}'))
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=get_last_state(session, user_id)))

    await bot.send_message(chat_id=user_id, text=f"Основные категории",
                           reply_markup=poll_keyboard)


@dp.callback_query_handler(lambda c: check_category(session, c.data))
async def category_command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    update_last_state(session, user_id, new_state=callback_query.data)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    categories = get_category(session, callback_query.data)
    parent_cat = categories[0]
    for cat in categories[1]:
        poll_keyboard.add(types.InlineKeyboardButton(text=cat.name, callback_data=f'{cat.command}'))
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=get_last_state(session, user_id)))
    await bot.send_message(chat_id=callback_query.from_user['id'], text=f"{parent_cat.name}",
                           reply_markup=poll_keyboard)


@dp.callback_query_handler(lambda c: check_show_product(session, c.data))
async def show_product_command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    command = callback_query.data
    update_last_state(session, user_id, new_state=command)
    product = get_product(session, command)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=get_last_state(session, user_id)))
    poll_keyboard.add(types.InlineKeyboardButton(text='Купить', callback_data=f'buy {command}'))
    caption = f"{product.name} \n {product.description}"
    image = get_image(session, product)
    update_last_product(session, user_id, command)
    await bot.send_photo(callback_query.from_user['id'], image.image,
                         caption=caption,
                         reply_markup=poll_keyboard)


@dp.callback_query_handler(lambda c: check_show_products(session, c.data))
async def show_products_command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    command = callback_query.data
    update_last_state(session, user_id, new_state=command)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    category = get_category(session, command)
    products = get_products(session, command)
    for product in products:
        poll_keyboard.add(types.InlineKeyboardButton(text=product.name, callback_data=f'{product.command}'))
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=get_last_state(session, user_id)))
    await bot.send_message(chat_id=callback_query.from_user['id'], text=f"{category[0].name}",
                           reply_markup=poll_keyboard)


if __name__ == "__main__":
    session = start_session()
    executor.start_polling(dp)
