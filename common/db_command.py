import json
from sqlalchemy.orm import sessionmaker
from .init_db import Product, Category, Image, bot_db, User


def check_start_category(session):
    instance = session.query(Category).filter(Category.status == 0).first()
    if instance:
        data = instance.command
    elif len(session.query(Category).all()) > 1:
        instance = session.query(Category).all()
        data = instance[-1].command
    else:
        data = None
    return data


def start_session():
    Session = sessionmaker(bind=bot_db)
    session = Session()
    return session


def add_object(session, object_request):
    new_object = object_request
    session.add(new_object)


def check_object(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        return None


def add_category(session, name, command, description, parent_category):
    check = check_object(session, Category, command=command)
    if check is None:
        new_category = Category(name, command, description, False, parent_category)
        if parent_category:
            new_category.parent_category.append(parent_category)
        add_object(session, new_category)
        return new_category
    else:
        if parent_category:
            check.parent_category.append(parent_category)
        return check


def add_product(session, name, description, command, cost, Category, update):
    check = check_object(session, Product, command=command)
    if check is None:
        new_product = Product(name, description, command, cost)
        new_product.category.append(Category)
        add_object(session, new_product)
        return new_product
    else:
        if update:
            check.name = name
            check.description = description
            check.command = command
            check.cost = cost
        check.category.append(Category)
        return check


def add_image(session, Product, image):
    new_image = Image(image, None)
    Product.images.append(new_image)
    add_object(session, new_image)


def update_status(Category, status):
    Category.status = status


def update_all_status(session):
    for instance in session.query(Category):
        instance.status = False
    session.commit()
