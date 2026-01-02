from datetime import datetime
from functools import wraps
close_reg = datetime(2026, 1, 15,3,0,0)
"""Декораторы для функций"""

def error_handler(func): #Обработчик ошибок
    async def wrapper(*args):
        try:
            await func(*args)
        except Exception as e:
            await print(e)
    return wrapper

def date(func):
    @wraps(func)
    async def wrapper(message,*args, **kwargs):
        if datetime.now()<close_reg:
            await func(message,*args, **kwargs)
        else:
            await message.answer("📅Регистрация на турнир закрыта!")
    return wrapper

