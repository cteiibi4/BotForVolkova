COMMANDS = {'about_company': {
        'father': 'start',
        'name': 'Узнать о бизнесе',
        'text': 'тут о бизнесе',
        'commands': ['my_story', '6_min', 'plan'],
    },
    'my_story': {
        'father': 'about_company',
        'name': 'Моя история',
        'text': '''Привет 👋🏽
Меня зовут Волкова Елена, я лидер компании GreenWay
Мой опыт в сетевом более 4-х лет 🌐

Сейчас я успешно совмещаю работу в найме и сетевой бизнес. А когда я только начинала, была в декрете, жила в небольшом городе и строила сеть без офиса, магазина и наставника в городе.
Именно поэтому в моей команде есть и мамы в декрете, и гос служащие, и работники в найме, и девчонки из небольших городков и деревень.
Бизнес в партнёрстве с GreenWay доступен каждому!

Моя команда из 3 стран и более 15 регионов России.

Здесь не нужны вложения.
Можно совмещать с любой другой деятельностью.
Доход с первого месяца - деньгами.
Нет потолка в доходе.
Бесплатная регистрация и обучение.

И запомни два важных правила: 
1. Сегодня ты можешь зарабатывать, не выходя из дома, просто используя смартфон.
2. Не думай, что зарабатывать ты сможешь только на том, в чем на данный момент разбираешься.

Набираю партнеров в первую линию
20+
Любой город''',
        'commands': ['want_in_command'],
    },
    '6_min': {
        'father': 'about_company',
        'name': 'Коротко за 6 минут',
        'text': '6 минут',
        'video': 'https://www.youtube.com/watch?v=it87JRX9qmY',
        'commands': ['want_in_command'],
    },
    'plan': {
        'father': 'about_company',
        'name': 'Маркетинг план',
        'text': '''Здесь можно подробно изучить маркетинг план компании.
Но лучше созвониться и я расскажу все простым доступным языком 😉

Если коротко и  без таблиц, то в первый месяц можно не сложно заработать 10-15 тыс руб. На третий-пятый месяц выйти на доход 40-50 тыс.руб. Это доступно всем с базовыми знаниями, которые даются на начальном этапе.

Дальше все зависит от твоих амбиций, ведь «потолка» в зарплате нет и у ТОП-лидеров она исчисляется в миллионах рублей в месяц.''',
        'file': 'common/Маркетинг-план.pdf',
        'commands': ['want_in_command'],
    },
}
# for data base
BASE = 'telebot.db'
# fro parser
BASE_URL = 'https://mygreenway.com'

