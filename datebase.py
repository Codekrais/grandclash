import json
import asyncio

import qrcode
from openpyxl import Workbook
from openpyxl.styles import Font
from qrcode import *
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from decorators import close_reg
async def make_note_into_db(chatid: str, tgid: str):
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
    if chatid not in data:
        data.update({
            chatid: {"blank": {},
                   "tgid": tgid
                   },
        })
    with open('db.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def send_reg_into_db(blank: dict, chatid: str):
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)

    data.get(chatid)["blank"] = blank

    # data.setdefault(tgid,{}).update({"blank": blank})

    # data.update({
    #     tgid:{"blank":blank
    #           },
    # })
    with open('db.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def get_reg_from_db(chatid: str):
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
    name = data.get(chatid)
    if name:
        blank = name.get("blank")
        if blank:
            return f"""
<b> ВАШ БЛАНК РЕГИСТРАЦИИ </b>

1️⃣ <b>ИМЯ И ФАМИЛИЯ🧑</b>: {blank.get("name")}

2️⃣ <b>КЛАСС🏫</b>: {blank.get("clas")}

3️⃣ <b>ID из CLASH ROYALE🪪</b>: {blank.get("clash_id")}

4️⃣ <b>ССЫЛКА НА ДОБАВЛЕНИЕ В ДРУЗЬЯ⛓️</b> {blank.get("link")}

5️⃣ <b>КОЛОДА🃏</b>: {blank.get("coloda")}

"""
    return False

async def remove_blank_from_db(chatid: str):
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)

    name = data.get(chatid)
    if name:
        blank = name.get("blank")
        if blank:
            data.get(chatid)["blank"] = {}
            with open('db.json', 'w', encoding='UTF-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return f"""✅Вы успешно удалили бланк регистрации"""
    return f"""⛔Вы не зарегистрированы"""

async def get_qr_code_from_db(chatid: str):
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
    name = data.get(chatid)
    if name:
        blank = name.get("blank")
        if blank:
            qr = QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=23,
                border=1,
            )
            qr.add_data(chatid)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            # img = Image.open("photo/obraz2.png")
            # x = 1154+5
            # y = 540+3
            # z = 1690
            # w = 1076
            # date = close_reg.strftime("%d Января %Y")
            # draw = ImageDraw.Draw(img)
            # font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            # draw.text((2050,332-20),date,(52,61,135), font=ImageFont.truetype("DejaVuSans-Bold.ttf", size=60))
            # img.paste(qr_img,(x,y))
            return qr_img.tobytes()
    return f"""⛔Вы не зарегистрированы"""
#########################################################################################################################################
"""
Для админки
|
|
|
"""
async def get_report_from_db():
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
    all_users = 0
    blank_count = 0
    for chatid in data:
        all_users += 1
        if data.get(chatid).get("blank"):
            blank_count += 1

    return f"""
<b>ОТЧЕТ ПО БД</b>:

<b>🧑КОЛ-ВО ПОЛЬЗОВАТЕЛЕЙ:</b> {all_users}

<b>✒️КОЛ-ВО ЗАРЕГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ:</b> {blank_count}
"""

async def get_mailing_list_from_db():
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
    return [x for x in data]

async def get_db_for_admin():
    with open("db.txt", "w") as f:
        pass
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
        with open("db.txt", "w", encoding="UTF-8") as f:
            for chatid in data:
                report = f"""1️⃣ TG USER NAME: {data.get(chatid).get("tgid")} 
2️⃣ ИМЯ И ФАМИЛИЯ🧑: {data.get(chatid)["blank"].get("name", "Отсутствует")}
3️⃣ КЛАСС🏫: {data.get(chatid)["blank"].get("clas", "Отсутствует")}
4️⃣ ID из CLASH ROYALE🪪: {data.get(chatid)["blank"].get("clash_id", "Отсутствует")}
5️⃣ ССЫЛКА НА ДОБАВЛЕНИЕ В ДРУЗЬЯ⛓️: {data.get(chatid)["blank"].get("link", "Отсутствует")}
6️⃣ КОЛОДА🃏: {data.get(chatid)["blank"].get("coloda", "Отсутствует")}\n
"""
                print(report, file=f)
    return True
async def get_excel_from_db():
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
    users_ls = [["ЧАТ-ID", "ЮЗЕРНЕЙМ", "ИМЯ И ФАИМЛИЯ", "КЛАСС", "CLASH ROYALE ID", "ССЫЛКА НА ДОБАВЛЕНИЕ В ДРУЗЬЯ", "КОЛОДА", "ПРИСУТСТВИЕ"]]
    for chatid in data:
        tgid = data.get(chatid).get("tgid")
        if data.get(chatid).get("blank"):
            name = data.get(chatid).get("blank").get("name")
            clas = data.get(chatid).get("blank").get("clas")
            clash_id = data.get(chatid).get("blank").get("clash_id")
            link = data.get(chatid).get("blank").get("link")
            coloda = data.get(chatid).get("blank").get("coloda")
            users_ls.append([chatid, tgid, name, clas, clash_id, link, coloda, " "])
    wb = Workbook()
    new_sheet = wb.active
    new_sheet.title = "Пользователи"
    for row in users_ls:
        new_sheet.append(row)
    new_sheet.column_dimensions["A"].width = 15
    new_sheet.column_dimensions["B"].width = 15
    new_sheet.column_dimensions["C"].width = 20
    new_sheet.column_dimensions["D"].width = 10
    new_sheet.column_dimensions["E"].width = 16
    new_sheet.column_dimensions["F"].width = 34
    new_sheet.column_dimensions["G"].width = 15
    new_sheet.column_dimensions["H"].width = 14
    new_sheet["A1"].font = Font(bold=True, name="Calibri")
    new_sheet["B1"].font = Font(bold=True, name="Calibri")
    new_sheet["C1"].font = Font(bold=True, name="Calibri")
    new_sheet["D1"].font = Font(bold=True, name="Calibri")
    new_sheet["E1"].font = Font(bold=True, name="Calibri")
    new_sheet["F1"].font = Font(bold=True, name="Calibri")
    new_sheet["G1"].font = Font(bold=True, name="Calibri")
    new_sheet["H1"].font = Font(bold=True, name="Calibri")
    wb.save('db.xlsx')
    return True
"""
|
|
|
Конец для админки
"""
#########################################################################################################################################