from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
back = [KeyboardButton(text="В главное меню❗")]
admin_back = [KeyboardButton(text="В главное меню панели❗")]

main = [
    [KeyboardButton(text="Регистрация🔗"),KeyboardButton(text="Техподдержка🔧")],
    [KeyboardButton(text="Обход Рунета🥷")]
]

blank = [
    [KeyboardButton(text = "Изменить регистрацию♻️"), KeyboardButton(text = "Удалить регистрацию🗑️")],
    back
]

delete_reg = [
    [KeyboardButton(text="✅Уверен"), KeyboardButton(text="❌Не уверен")]
]

start_reg = [
    [KeyboardButton(text = "Начать регистрацию✅")],
    [KeyboardButton(text = "Посмотреть бланк регистрации📋")],
    #[KeyboardButton(text = "Сколько осталось до конца регистрации⁉️")],
    back
]

cancel_to_main = [
    back
]
admin = [
    [KeyboardButton(text="Отчет по БД📝"),KeyboardButton(text="Рассылка🔃"),KeyboardButton(text="Получить БД🗃️")],
    [KeyboardButton(text="RUNTIME бота⏰")],
    [KeyboardButton(text="Выйти из панели⛔")]
]

cancel_to_main_admin = [
    admin_back
]
start_reg_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=start_reg)
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=main)
blank_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=blank)
delete_reg_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=delete_reg)
cancel_to_main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=cancel_to_main)
admin_main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=admin)
cancel_to_main_admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=cancel_to_main_admin)
