from aiogram import Bot, Dispatcher, executor, types

from common.common import COMMANDS
from common.db_command import start_session
from common.send_email import send_email
from common.bot_command import get_parent_categorys, check_category, get_category, check_show_products, get_products, \
    get_product, check_show_product, get_image, update_last_state, get_last_state, update_user_phone, create_user_state, \
    check_user_data, update_user_name, get_user_answer, update_last_product, get_user, set_last_message, \
    get_last_message, check_buy_product

from common.check_data import check_phone, check_name
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def prepare_message(state, callback_query):
    user_id = callback_query.from_user['id']
    user = get_user(session, user_id)
    last_msg = get_last_message(user)
    update_last_state(session, user)
    update_last_product(user, state)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"{get_last_state(user)}"))
    poll_keyboard.add(types.InlineKeyboardButton(text='На главную', callback_data='start'))
    if check_user_data(user):
        if send_email(session, user):
            message = await bot.send_message(chat_id=user_id, text=get_user_answer(user),
                                             reply_markup=poll_keyboard)
    else:
        message = await bot.send_message(chat_id=user_id, text=f"Введите номер своего телефона для связи",
                                         reply_markup=poll_keyboard)
    set_last_message(session, user, message["message_id"])
    await bot.delete_message(user.user_id, last_msg)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота")])


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    message_id = message["message_id"]
    user = get_user(session, message['from']['id'])
    create_user_state(session, user)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.InlineKeyboardButton(text='Узнать о бизнесе', callback_data='about_company'))
    poll_keyboard.add(types.InlineKeyboardButton(text='Каталог товаров', callback_data='catalog'))
    message = await bot.send_message(chat_id=user.user_id, text="Главное меню", reply_markup=poll_keyboard)
    await bot.delete_message(user.user_id, message_id)
    set_last_message(session, user, message["message_id"])


@dp.callback_query_handler(lambda c: c.data == 'start')
async def main_menu(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    user = get_user(session, user_id)
    last_msg = get_last_message(user)
    create_user_state(session, user)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.InlineKeyboardButton(text='Узнать о бизнесе', callback_data='about_company'))
    poll_keyboard.add(types.InlineKeyboardButton(text='Каталог товаров', callback_data='catalog'))
    message = await bot.send_message(chat_id=user_id, text="Главное меню", reply_markup=poll_keyboard)
    set_last_message(session, user, message["message_id"])
    await bot.delete_message(user.user_id, last_msg)


@dp.message_handler(lambda message: check_phone(message.text))
async def get_phone_command(message: types.Message):
    message_id = message["message_id"]
    user_id = message['from']['id']
    user = get_user(session, user_id)
    update_user_phone(session, user, message.text)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"{get_last_state(user)}"))
    poll_keyboard.add(types.InlineKeyboardButton(text='На главную', callback_data='start'))
    await bot.delete_message(user.user_id, get_last_message(user))
    if check_user_data(user):
        send_email(session, user)
        message = await bot.send_message(chat_id=user_id, text=get_user_answer(user),
                                         reply_markup=poll_keyboard)
    else:
        message = await bot.send_message(chat_id=user_id, text="Введите свое имя", reply_markup=poll_keyboard)
    await bot.delete_message(user.user_id, message_id)
    set_last_message(session, user, message["message_id"])


@dp.message_handler(lambda message: check_name(message.text))
async def get_name_command(message: types.Message):
    message_id = message["message_id"]
    user_id = message['from']['id']
    user = get_user(session, user_id)
    update_user_name(session, user, message.text)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"{get_last_state(user)}"))
    poll_keyboard.add(types.InlineKeyboardButton(text='На главную', callback_data='start'))
    await bot.delete_message(user.user_id, get_last_message(user))
    if check_user_data(user):
        send_email(session, user)
        message = await bot.send_message(chat_id=user_id, text=get_user_answer(user),
                                         reply_markup=poll_keyboard)
    else:
        message = await bot.send_message(chat_id=user_id, text="Введите номер телефона", reply_markup=poll_keyboard)
    await bot.delete_message(user.user_id, message_id)
    set_last_message(session, user, message["message_id"])


@dp.callback_query_handler(lambda c: c.data == 'want_in_command' or check_buy_product(c.data))
async def want_in_command(callback_query: types.CallbackQuery):
    if callback_query.data == 'want_in_command':
        await prepare_message('want_in_command', callback_query)
    else:
        await prepare_message(callback_query.data.split(':')[-1], callback_query)


@dp.callback_query_handler(lambda c: c.data and c.data in COMMANDS)
async def command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    user = get_user(session, user_id)
    last_msg = get_last_message(user)
    command = callback_query.data
    update_last_state(session, user, new_state=command)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    video = COMMANDS[command].get('video', None)
    text = COMMANDS[command].get('text', None)
    for com in COMMANDS[command]['commands']:
        if com in COMMANDS:
            poll_keyboard.add(types.InlineKeyboardButton(text=COMMANDS[com]['name'], callback_data=f'{com}'))
        elif com == 'want_in_command':
            poll_keyboard.add(types.InlineKeyboardButton(text='Хочу в команду', callback_data=f'{com}'))
    if COMMANDS[command].get('father', None):
        poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f"{get_last_state(user)}"))
    if video:
        message = await bot.send_message(chat_id=user_id, text=f"{text}\n{video}{video}",
                                       reply_markup=poll_keyboard)
    else:
        message = await bot.send_message(chat_id=user_id, text=f"{text}", reply_markup=poll_keyboard)
    set_last_message(session, user, message["message_id"])
    await bot.delete_message(user.user_id, last_msg)


@dp.callback_query_handler(lambda c: c.data == 'catalog')
async def catalog_command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    user = get_user(session, user_id)
    last_msg = get_last_message(user)
    update_last_state(session, user, new_state=callback_query.data)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    categories = get_parent_categorys(session)
    for cat in categories:
        poll_keyboard.add(types.InlineKeyboardButton(text=cat.name, callback_data=f'{cat.command}'))
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=get_last_state(user)))
    message = await bot.send_message(chat_id=user_id, text=f"Основные категории",
                                     reply_markup=poll_keyboard)
    set_last_message(session, user, message["message_id"])
    await bot.delete_message(user.user_id, last_msg)


@dp.callback_query_handler(lambda c: check_category(session, c.data))
async def category_command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    user = get_user(session, user_id)
    last_msg = get_last_message(user)
    update_last_state(session, user, new_state=callback_query.data)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    categories = get_category(session, callback_query.data)
    parent_cat = categories[0]
    for cat in categories[1]:
        poll_keyboard.add(types.InlineKeyboardButton(text=cat.name, callback_data=f'{cat.command}'))
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=get_last_state(user)))
    message = await bot.send_message(chat_id=callback_query.from_user['id'], text=f"{parent_cat.name}",
                                     reply_markup=poll_keyboard)
    set_last_message(session, user, message["message_id"])
    await bot.delete_message(user.user_id, last_msg)


@dp.callback_query_handler(lambda c: check_show_product(session, c.data))
async def show_product_command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    user = get_user(session, user_id)
    last_msg = get_last_message(user)
    command = callback_query.data
    update_last_state(session, user, new_state=command)
    product = get_product(session, command)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=get_last_state(user)))
    poll_keyboard.add(types.InlineKeyboardButton(text='Купить', callback_data=f'buy:{command}'))
    caption = f"{product.name} \n {product.description}"
    image = get_image(session, product)
    update_last_product(user, command)
    message = await bot.send_photo(callback_query.from_user['id'], image.image,
                                   caption=caption,
                                   reply_markup=poll_keyboard)
    set_last_message(session, user, message["message_id"])
    await bot.delete_message(user.user_id, last_msg)


@dp.callback_query_handler(lambda c: check_show_products(session, c.data))
async def show_products_command(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user['id']
    user = get_user(session, user_id)
    last_msg = get_last_message(user)
    command = callback_query.data
    update_last_state(session, user, new_state=command)
    poll_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    category = get_category(session, command)
    products = get_products(session, command)
    for product in products:
        poll_keyboard.add(types.InlineKeyboardButton(text=product.name, callback_data=f'{product.command}'))
    poll_keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=get_last_state(user)))
    message = await bot.send_message(chat_id=callback_query.from_user['id'], text=f"{category[0].name}",
                                     reply_markup=poll_keyboard)
    set_last_message(session, user, message["message_id"])
    await bot.delete_message(user.user_id, last_msg)


if __name__ == "__main__":
    session = start_session()
    executor.start_polling(dp)
