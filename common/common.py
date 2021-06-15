COMMANDS = {'about_company': {
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
# for data base
BASE = 'telebot.db'
# fro parser
BASE_URL = 'https://mygreenway.com'

