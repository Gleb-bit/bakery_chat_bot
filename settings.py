GROUP_ID = 204760990
TOKEN = '3a96ef7743ef28fc6e6ebc73b7aa4d98120fa7bc37bb7b31d68495c5e53ba86a63dea88b657738b2c6c04'

user = 'postgres'
db_name = 'postgres'

DB_CONFIG = dict(
    user=user,
    database=db_name,
    host='localhost',
    port='5432',
)

INTENTS = [
    {
        'name': 'Сообщение помощи',
        'tokens': ('help', 'помощь'),
        'scenario': None,
        'answer': 'Здравствуйте, я бот для заказа выпечки. Если хотите начать выбор товаров, напишите /start'
    },
    {
        'name': 'Начало сценария',
        'tokens': '/start',
        'scenario': 'start_scenario',
        'answer': None
    },
]
SCENARIOS = {
    'first_step': 1,
    'steps': {
        1: {
            'text': 'Хорошо, давайте начнём. Пожалуйста, выберите категорию, о которой хотели бы узнать',
            'failure_text': 'К сожалению, такой категории нет',
            'handler': 'handle_first_keyboard',
            'next_step': 2,
        },
        2: {
            'text': 'Выберите продукт',
            'failure_text': 'К сожалению, данного продукта нет',
            'handler': 'handle_second_keyboard',
            'next_step': 3,
        },
        3: {
            'text': 'Вот описание и фото выбранного продукта:',
            'failure_text': 'Вы ввели неправильную дату, либо на данную дату нет ни одного рейса',
            'image': True,
            'handler': 'handle_third_keyboard',
            'next_step': None
        }
    }
}

BACK_ANSWER = 'Хорошо, вернёмся на страницу назад'
BACK_TO_MAIN_ANSWER = 'Хорошо, вернёмся на главную'
DEFAULT_ANSWER = 'Простите, не понял вас. я бот для заказа выпечки. Могу помочь вам выбрать товар'
