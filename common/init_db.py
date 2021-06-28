from sqlalchemy import create_engine, Table, String, Boolean, Date, Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .common import BASE


bot_db = create_engine(f'sqlite:///{BASE}', echo=False)

TeleBot = declarative_base()

menu_table = Table('menu', TeleBot.metadata,
                   Column('product', String, ForeignKey('product.command')),
                   Column('category', String, ForeignKey('category.name')),
                   )

relation = Table('relation', TeleBot.metadata,
                 Column('category_a_com', String, ForeignKey('category.command'),
                        primary_key=True),
                 Column('category_b_com', String, ForeignKey('category.command'),
                        primary_key=True)
                 )


class Product(TeleBot):
    __tablename__ = 'product'
    name = Column(String)
    description = Column(String)
    command = Column(String, primary_key=True, unique=True)
    cost = Column(Integer)
    category = relationship('Category',
                            secondary=menu_table,
                            back_populates='products')
    images = relationship('Image', back_populates='product')

    def __init__(self, name, description, command, cost):
        self.name = name
        self.description = description
        self.command = command
        self.cost = cost


class Category(TeleBot):
    __tablename__ = 'category'

    name = Column(String, unique=True)
    command = Column(String, unique=True, primary_key=True)
    description = Column(String)
    products = relationship('Product',
                            secondary=menu_table,
                            back_populates='category')
    parent_category = relationship("Category", secondary=relation,
                                   primaryjoin=command == relation.c.category_a_com,
                                   secondaryjoin=command == relation.c.category_b_com,
                                   )
    status = Column(Boolean, default=0)

    def __init__(self, name, command, description, status, parent_name):
        self.name = name
        self.command = command
        self.description = description
        self.status = status
        # self.parent_category_name = parent_name


class Image(TeleBot):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    image = Column(String)
    telegram_id = Column(String)
    product = relationship('Product', back_populates='images')
    part_id = Column(String, ForeignKey('product.command'))

    def __init__(self, image, telegram_id):
        self.image = image
        self.telegram_id = telegram_id


class User(TeleBot):
    __tablename__ = 'user'
    path = Column(String)
    user_id = Column(String, primary_key=True, unique=True)
    name = Column(String)
    phone = Column(String)
    last_product = Column(String)
    last_message = Column(String)

    def __init__(self, path, client_id):
        self.path = path
        self.user_id = client_id


TeleBot.metadata.create_all(bot_db)
