import json
async def make_note_into_db(tgid: str, chatid):
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
    if tgid not in data:
        data.update({
            tgid: {"blank": {},
                   "chatid": chatid
                   },
        })
    with open('db.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def send_reg_into_db(blank: dict, tgid: str):
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)

    data.get(tgid)["blank"] = blank

    # data.setdefault(tgid,{}).update({"blank": blank})

    # data.update({
    #     tgid:{"blank":blank
    #           },
    # })
    with open('db.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def get_reg_from_db(tgid: str):
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
    name = data.get(tgid)
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

async def remove_blank_from_db(tgid: str):
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)

    name = data.get(tgid)
    if name:
        blank = name.get("blank")
        if blank:
            data.get(tgid)["blank"] = {}
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
    for usid in data:
        all_users += 1
        if data.get(usid).get("blank"):
            blank_count += 1

    return f"""
<b>ОТЧЕТ ПО БАЗЕ ДАННЫХ</b>:

<b>🧑КОЛ-ВО ПОЛЬЗОВАТЕЛЕЙ:</b> {all_users}

<b>✒️КОЛ-ВО ЗАРЕГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ:</b> {blank_count}
"""

async def get_mailing_list_from_db():
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
    mailing_list = []
    for i in data:
        mailing_list.append(int(data[i].get("chatid")))
    return mailing_list

async def get_db_for_admin():
    with open("db.txt", "w") as f:
        pass
    with open('db.json', encoding='UTF-8') as f:
        data = json.load(f)
        with open("db.txt", "w", encoding="UTF-8") as f:
            for usid in data:
                report = f"""1️⃣ TG USER NAME: {usid} 
2️⃣ ИМЯ И ФАМИЛИЯ🧑: {data.get(usid)["blank"].get("name", "Отсутствует")}
3️⃣ КЛАСС🏫: {data.get(usid)["blank"].get("clas", "Отсутствует")}
4️⃣ ID из CLASH ROYALE🪪: {data.get(usid)["blank"].get("clash_id", "Отсутствует")}
5️⃣ ССЫЛКА НА ДОБАВЛЕНИЕ В ДРУЗЬЯ⛓️: {data.get(usid)["blank"].get("link", "Отсутствует")}
6️⃣ КОЛОДА🃏: {data.get(usid)["blank"].get("coloda", "Отсутствует")}\n
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