import os
from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Bot
import keydoard as kb
from datebase import *
from re import fullmatch
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from decorators import *
from keydoard import cancel_to_main, cancel_to_main_keyboard, start_reg_keyboard

load_dotenv()
LOGIN = str(os.getenv("LOGIN"))
PASSWORD = str(os.getenv("PASSWORD"))

uptime = datetime.now()

router = Router()

class Reg(StatesGroup):
    name = State()
    clas = State()
    clash_id = State()
    link = State()
    coloda = State()
class Admin(StatesGroup):
    isAdmin = State()
    mail = State()

"""Стартовое сообщение"""
@router.message(Command('start'))
async def hi(message: Message, state: FSMContext):
    await state.clear()
    await make_note_into_db(str(message.from_user.id),f"@{message.from_user.username}")
    await message.answer(f"""
Этот бот создан для регистрации на участие в турнире по игре Clash Royale в Пивоваровской школе

Разработчик: @codebykrais
""", reply_markup=kb.main_keyboard)

@router.message(F.text == "Регистрация🔗")
async def reg(message: Message):
    await message.answer(f"""
Отлично, ты решил зарегистрироваться! Для регистрации тебе потребуются:

1️⃣ <b>ИМЯ И ФАМИЛИЯ🧑</b>:
(с заглавной буквы через пробел, пример: Иван Иванов)

2️⃣ <b>КЛАСС🏫</b>:
(сначало число, а потом заглавная буква без пробела, пример: 10А, 5Е, 6Б и так далее)

3️⃣ <b>ID ИЗ CLASH ROYALE🪪</b>:
(он начинается с #, пример: #111111111)

4️⃣ <b>ССЫЛКА НА ДОБАВЛЕНИЕ В ДРУЗЬЯ⛓️</b>

5️⃣ <b>КОЛОДА🃏</b>:
(она должна состоять из 8 карт, около некотрых в скобках нужно указать эво/герой/чемпион.
Пример: один, два (герой), три (чемпион), четыре, пять (эво), шесть, семь, восемь)
""", reply_markup=kb.start_reg_keyboard)


"""Начало меню регистрации"""
@router.message(F.text.in_({"В главное меню❗","Выйти из панели⛔"}))
async def reg(message: Message, state: FSMContext):
    await state.clear()
    await make_note_into_db(str(message.from_user.id), f"@{message.from_user.username}")
    await message.answer(f"""
💾Вы перешли в главное меню! Выберите нужный пункт в меню снизу!
""", reply_markup=kb.main_keyboard)

@router.message(F.text.in_({"Посмотреть бланк регистрации📋","❌Не уверен"}))
async def reg(message: Message):
    blank = await get_reg_from_db(str(message.from_user.id))
    if blank:
        await message.answer(f"""{blank}""", reply_markup=kb.blank_keyboard)
    else: await message.answer(f"""⛔Вы не зарегистрированы""", reply_markup=start_reg_keyboard)

@router.message(F.text.in_({"Сколько осталось до конца регистрации⁉️"}))
@date
async def reg(message: Message):
    raz = close_reg - datetime.now()
    await message.answer(f"""
До конца регистрации осталось {raz.days} дней, {raz.seconds // 3600} часов, {(raz.seconds % 3600) // 60} минут
""", reply_markup=kb.start_reg_keyboard)

@router.message(F.text == "Удалить регистрацию🗑️")
async def reg(message: Message):
    await message.answer("⁉️Вы уверены, что хотите удалить регистрацию?", reply_markup=kb.delete_reg_keyboard)

@router.message(F.text == "✅Уверен")
async def reg(message: Message):
    recv = await remove_blank_from_db(str(message.from_user.id))
    await message.answer(f"""
{recv}
""", reply_markup=start_reg_keyboard)

@router.message(F.text == "Обход Рунета🥷")
async def reg(message: Message):
    await message.answer(f"""
Обход Рунета🥷: @wlbypass_bot
""", reply_markup=kb.main_keyboard)

@router.message(F.text == "Техподдержка🔧")
async def reg(message: Message):
    await message.answer(f"""
Вопросы по турниру: @curs3dik
Вопросы по боту и техчасти: @endurra
""", reply_markup=kb.main_keyboard)


#########################################################################################################################################
"""Конец меню регистрации, начало бланка регистрации
|
|
|
"""
@router.message(F.text.in_({"Начать регистрацию✅", "Изменить регистрацию♻️"}))
#@date
async def clash_id(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer(f"""1️⃣ Введите ваше имя и фамилию""", reply_markup=cancel_to_main_keyboard)

@router.message(Reg.name)
async def link(message: Message, state: FSMContext):
    if fullmatch(r"\b[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+\b", message.text):
        await state.update_data(name=message.text)
        await state.set_state(Reg.clas)
        await message.answer(f"""2️⃣ Введите ваш класс""",
                             reply_markup=cancel_to_main_keyboard)
    else:
        await message.answer(f"""⛔Вы ввели некорректное имя и фамилию! Введите корректные данные (Имя с заглавной и фамилия с заглавной буквы, пример: Иван Иванов)""", reply_markup=cancel_to_main_keyboard)

@router.message(Reg.clas)
async def link(message: Message, state: FSMContext):
    if fullmatch(r"^(1[01]|[5-9])[А-ЯЁ]$", message.text):
        await state.update_data(clas=message.text)
        await state.set_state(Reg.clash_id)
        await message.answer(f"""3️⃣ Введите ваш ID из Clash Royale""",
                             reply_markup=cancel_to_main_keyboard)
    else:
        await message.answer(f"""⛔Вы ввели некорректный класс! Введите корреткные данные (сначало число, а потом заглвная буква без пробела, пример корректного ввода: 10А, 5Е, 6Б и так далее)⛔""", reply_markup=cancel_to_main_keyboard)

@router.message(Reg.clash_id)
async def link(message: Message, state: FSMContext):
    if fullmatch(r"#[A-z0-9]{9}", message.text):
        await state.update_data(clash_id=message.text)
        await state.set_state(Reg.link)
        await message.answer(f"""4️⃣ Введите вашу ссылку на добавление в друзья Clash Royale""",reply_markup=cancel_to_main_keyboard)
    else:
        await message.answer(f"""⛔Вы ввели некорректный ID! Введите корректный (он начинается #, пример: #111111111)""",reply_markup=cancel_to_main_keyboard)

@router.message(Reg.link)
async def coloda(message: Message, state: FSMContext):
    if fullmatch(r"https://link\.clashroyale\.com/invite/friend/.*", message.text):
        await state.update_data(link=message.text)
        await state.set_state(Reg.coloda)
        await message.answer(f"""5️⃣ Введите состав вашей колоды""",reply_markup=cancel_to_main_keyboard)
    else:
        await message.answer(f"""⛔Вы ввели некорректную ссылку! Введите корректную ссылку""", reply_markup=cancel_to_main_keyboard)

@router.message(Reg.coloda)
async def last(message: Message, state: FSMContext):
    if fullmatch(r'^(?:[^,()]+(?:\s+[^,()]+)*)(?:\s*\([^)]*\))?(?:,\s*(?:[^,()]+(?:\s+[^,()]+)*)(?:\s*\([^)]*\))?){7}$', message.text):
        await state.update_data(coloda=message.text)
        blank = await state.get_data()
        await send_reg_into_db(blank, str(message.from_user.id))
        await message.answer(f"""✅Вы успешно закончили регистрацию!""",reply_markup=kb.main_keyboard)
        await state.clear()
    else: await message.answer(f"""⛔Вы ввели некорректную колоду! Введите корректную (она должна состоять из 8 карт, около некотрых в скобках нужно укзаать эво/герой/чемпион.
Пример: один, два (герой), три (чемпион), четыре, пять (эво), шесть, семь, восемь)""", reply_markup=cancel_to_main_keyboard)
"""
|
|
|
Конец бланка регистрации"""
#########################################################################################################################################


#########################################################################################################################################
"""
Логика админ-панели
|
|
|
"""
@router.message(Command('login_in_admin_panel'))
async def admin_login(message: Message, state: FSMContext):
    try:
        login = message.text.split()[1]
        password = message.text.split()[2]
    except IndexError:
        login = None
        password = None
    if login == LOGIN and password == PASSWORD:
        await state.clear()
        await state.set_state(Admin.isAdmin)
        await message.answer(f"""👨‍💻Вы успешно авторизовались в админ-панель""",reply_markup=kb.admin_main_keyboard)

@router.message(Admin.isAdmin, F.text == "Отчет по БД📝")
async def adm(message: Message, state: FSMContext):
    report = await get_report_from_db()
    await message.answer(report, reply_markup=kb.admin_main_keyboard)

@router.message(Admin.isAdmin, F.text == "Рассылка🔃")
async def adm(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(Admin.mail)
    await message.answer("🧾Введите текст рассылки", reply_markup=kb.cancel_to_main_admin_keyboard)

@router.message(Admin.mail, F.text != "В главное меню панели❗")
async def adm(message: Message, state: FSMContext, bot: Bot):
    mailing_list = await get_mailing_list_from_db()
    count = 0
    err = 0
    for id in mailing_list:
        try:
            await bot.send_message(chat_id=id, text=message.text)
            count += 1
        except:
            err += 1
    await state.set_state(Admin.isAdmin)
    await message.answer(f'''✅Рассылка завершена
Cообщение было отправлено {count} пользователям, {err} пользователей сообщение не получили''', reply_markup=kb.admin_main_keyboard)

@router.message(Admin.isAdmin, F.text == "Получить БД🗃️")
async def adm(message: Message, state: FSMContext, bot: Bot):
    recv = await get_db_for_admin()
    if recv:
        await message.answer_document(FSInputFile("db.txt"),caption="🗃️Сформированная БД")

@router.message(Admin.isAdmin, F.text == "RUNTIME бота⏰")
async def adm(message: Message, state: FSMContext, bot: Bot):
    runtime = datetime.now() - uptime
    await message.answer(f"""⏰С момента запуска бота прошло {runtime.days} дней, {runtime.seconds // 3600} часов, {(runtime.seconds % 3600) // 60} минут, {runtime.seconds % 60} секунд""", reply_markup=kb.admin_main_keyboard)

@router.message(Admin.isAdmin, F.text == "Excel отчет📗")
async def adm(message: Message, state: FSMContext, bot: Bot):
    recv = await get_excel_from_db()
    if recv:
        await message.answer_document(FSInputFile("db.xlsx"),caption="📗Exel отчет")


@router.message(Admin.isAdmin and Admin.mail, F.text == "В главное меню панели❗")
async def adm(message: Message, state: FSMContext):
    await state.set_state(Admin.isAdmin)
    await message.answer("Вы перешли в главное меню админ-панели", reply_markup=kb.admin_main_keyboard)

"""
|
|
|
Конец логики админ-панели
"""
#########################################################################################################################################