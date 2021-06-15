import json
import re

from .init_db import Category, User, Product, Image
from .db_command import check_object, add_object


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


def get_last_state(session, user_id):
    state = session.query(User).filter(User.user_id == user_id).first()
    result = json.loads(state.path)
    # print(result)
    if len(result) > 1:
        return result[-2]
    return result[-1]


def update_last_state(session, user_id, new_state=None):
    state = session.query(User).filter(User.user_id == user_id).first()
    path = json.loads(state.path)
    if new_state and new_state not in path:
        path.append(new_state)
    else:
        path.pop()
    print(path)
    state.path = json.dumps(path)
    session.commit()
    return path


def update_user_phone(session, user_id, phone):
    user = session.query(User).filter(User.user_id == user_id).first()
    user.phone = phone
    session.commit()


def update_user_name(session, user_id, name):
    user = session.query(User).filter(User.user_id == user_id).first()
    user.name = name
    session.commit()


def check_user_data(session, user_id):
    user = session.query(User).filter(User.user_id == user_id).first()
    if user.phone and user.name:
        return True
    return False


def create_user_state(session, user_id):
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        client_path = User(json.dumps(['start']), user_id)
        add_object(session, client_path)
    else:
        user.path = json.dumps(['start'])
    session.commit()


def get_user_answer(session, user_id):
    user = check_object(session, User, user_id=user_id)
    if user.last_product == 'want_in_command':
        return f'Спасибо {user.name}, в ближайшее время с вами свяжутся'
    return f'Спасибо {user.name},в ближайшее время с вами свяжутся для обсуждения деталей заказа'


def update_last_product(session, user_id, last_product):
    user = session.query(User).filter(User.user_id == user_id).first()
    user.last_product = last_product
