import json
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
    return f"""⛔Вы еще не зарегистрированы"""

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

"""
|
|
|
Конец для админки
"""
#########################################################################################################################################