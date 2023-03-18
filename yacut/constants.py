from re import escape
from string import ascii_letters, digits

RANDOM_SYMBOLS = ascii_letters + digits
REGEXP = rf'^[{escape(RANDOM_SYMBOLS)}]+$'
LENGTH_OF_ORIGINAL_URL = 1024
LENGTH_OF_RANDOM_URL = 6
LENGTH_OF_SHORT_URL = 16

LONG_URL = 'Длинная ссылка'
SHORT_URL = 'Ваш вариант короткой ссылки'

ID_NO_FOUND = 'Указанный id не найден'
USED_NAME = 'Имя {name} уже занято!'
