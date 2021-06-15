import re


def check_phone(message):
    reg_exp = '^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    if re.findall(reg_exp, message):
        return True
    return False


def check_name(message):
    reg_exp = '\w+\s*\w*'
    if re.findall(reg_exp, message):
        return True
    return False
