import smtplib
from .init_db import Product
from config import HOST, USERNAME, PASSWORD, FROM, TO


def send_email(session, User):
    if User.last_product == 'want_in_command':
        body = f'{User.name}, хочет в команду. \n Телефон:{User.phone}'
        subject = f'{User.name} хочет в комманду'
    else:
        product = session.query(Product).filter(Product.command == User.last_product).first()
        subject = f'{User.name} хочет в купить товар {product.name}'
        body = f'{User.name}, хочет заказать товар {product.name} № {product.command}. \n Телефон:{User.phone}'
    msg = "\r\n".join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % subject,
        "",
        body
    ))
    server = smtplib.SMTP_SSL(HOST, 465)
    server.login(USERNAME, PASSWORD)
    server.sendmail(FROM, [TO], msg.encode('utf-8'))
    server.quit()
    return True
