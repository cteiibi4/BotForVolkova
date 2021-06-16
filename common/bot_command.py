import json
import re

from .init_db import Category, User, Product, Image
from .db_command import add_object


def get_parent_categorys(session):
    return session.query(Category).filter(Category.parent_category == None).order_by(Category.name)


def get_category(session, command):
    parent_cat = session.query(Category).filter(Category.command == command).first()
    return parent_cat, sorted(session.query(Category).filter(Category.parent_category.contains(parent_cat)).all(), key=lambda x: x.name)


def check_category(session, command):
    res = session.query(Category).filter(Category.command == command).first()
    if res and not res.parent_category:
        if not session.query(Product).filter(Product.category.contains(res)).all():
            return True
    return False


def check_show_products(session, command):
    res = session.query(Category).filter(Category.command == command).first()
    products = session.query(Product).filter(Product.category.contains(res)).all()
    if res and products:
        return True
    return False


def check_show_product(session, command):
    res = session.query(Product).filter(Product.command == command).all()
    if res:
        return True
    return False


def get_product(session, command):
    return session.query(Product).filter(Product.command == command).first()


def get_products(session, command):
    cat = session.query(Category).filter(Category.command == command).first()
    products = session.query(Product).filter(Product.category.contains(cat)).all()
    return sorted(products, key=lambda x: x.name)


def get_image(session, Product):
    return session.query(Image).filter(Image.product == Product).first()


def get_last_state(User):
    result = json.loads(User.path)
    if len(result) > 1:
        return result[-2]
    return ['start']


def update_last_state(session, User, new_state=None):
    path = json.loads(User.path)
    if new_state and new_state not in path:
        path.append(new_state)
    else:
        path.pop()
    User.path = json.dumps(path)
    session.commit()
    return path


def update_user_phone(session, User, phone):
    User.phone = phone
    session.commit()


def update_user_name(session, User, name):
    User.name = name
    session.commit()


def check_user_data(User):
    if User.phone and User.name:
        return True
    return False


def create_user_state(session, User):
    User.path = json.dumps(['start'])
    session.commit()


def get_user_answer(User):
    if User.last_product == 'want_in_command':
        return f'Спасибо {User.name}, в ближайшее время с вами свяжутся'
    return f'Спасибо {User.name},в ближайшее время с вами свяжутся для обсуждения деталей заказа'


def update_last_product(User, last_product):
    User.last_product = last_product


def set_last_message(session, User, message_id):
    User.last_message = message_id
    session.commit()


def get_last_message(User):
    if User.last_message:
        return User.last_message


def get_user(session, user_id):
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        user = User(json.dumps(['start']), user_id)
        add_object(session, user)
    session.commit()
    return user


def check_buy_product(command):
    if command.split(':')[0] == 'buy':
        return True
    return False
