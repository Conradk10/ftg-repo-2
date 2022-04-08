# -*- coding: utf-8 -*-
import os
import datetime
from .. import loader, utils


@loader.tds
class SirenaInfoMod(loader.Module):
    """Модуль массового оповещения о сиренах в Днепре"""
    strings = {'name': 'SirenaInfo'}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    async def sinfocmd(self, message):
        """.sinfo <clearall> - удалить чаты
        .sinfo <listall> - вывести все чаты
        .sinfo <on> - добавить текущий чат
        .sinfo <off> - удалить текущий чат"""

        chats_data = self.db.get("SirenaInfo", "chats", [])

        chat_id = message.chat_id
        args = utils.get_args_raw(message)

        if args == "clearall":
            self.db.set("SirenaInfo", "chats", [])
            return await message.edit("<b>[Sirena Info]</b> Все настройки чатов сброшены")

        elif args == "listall":
            return await message.edit(f"<b>[Sirena Info]</b> Все чаты в базе данных:\n{chats_data}")

        elif args == "on":
            if chat_id not in chats_data:
                chats_data.append(chat_id)
                self.db.set("SirenaInfo", "chats", chats_data)
                return await message.edit(f"<b>[Sirena Info]</b> Чат добавлен успешно!\n\n"
                                          f"Все чаты в базе данных:\n{chats_data}")
            else:
                return await message.edit(f"<b>[Sirena Info]</b> Чат уже был добавлен!\n\n"
                                          f"Все чаты в базе данных:\n{chats_data}")

        elif args == "off":
            if chat_id in chats_data:
                chats_data.remove(chat_id)
                self.db.set("SirenaInfo", "chats", chats_data)
                return await message.edit(f"<b>[Sirena Info]</b> Чат успешно удален!\n\n"
                                          f"Все чаты в базе данных:\n{chats_data}")
            else:
                return await message.edit(f"<b>[Sirena Info]</b> Чат уже был удален!\n\n"
                                          f"Все чаты в базе данных:\n{chats_data}")
        else:
            return await message.edit("<b>[Sirena Info]</b> Ни один аргумент не выбран!")

    async def watcher(self, message):
        if message.text.lower() in ['!карта тревог', '!карта тревоги', '!карта сирен', '!карта сирены', '!карта',
                                    '! карта тревог', '! карта тревоги', '! карта сирен', '! карта сирены',
                                    '! карта', '/map', '/sirena']:
            msg = await message.respond(f"<b>[Sirena Info]</b> Завантажую мапу повітряних тривог...",
                                        reply_to=message.id)
            stream = os.popen('node /home/pi/misc-files/make-screenshot.js')
            output = stream.read()
            print(output)
            await msg.delete()
            now = datetime.datetime.now().strftime("%d %b, %H:%M")
            await message.client.send_file(message.chat_id, file='/home/pi/misc-files/webshot.jpg',
                                           caption=f'<b>[Sirena Info]</b> Мапа повітряних тривог станом на {now}',
                                           reply_to=message.id)
            await message.client.send_message(121020442, output)

        if message.text.lower() in ['/alerts', '/alert', '/alarm', '/alarms', '/achtung', 'ахтунг']:
            msg = await message.respond(f"<b>[Sirena Info]</b> Завантажую перелік активних повітряних тривог...",
                                        reply_to=message.id)
            stream = os.popen('node /home/pi/misc-files/view-alerts.js')
            output = stream.read()
            output = output.replace('</div>', "")
            output = output.split('<div class="col col-1">')
            text = "<b>[Sirena Info]</b> Перелік активних повітряних тривог:\n" \
                   "🚨 Регіон; ⌚️ Час початку; ⏳ Тривалість\n\n"
            output.pop(0)
            output.pop(0)
            for e in output:
                text += e.replace('<div class="col col-2">', '; ⌚ ').replace('<div class="col col-3">', '; ⏳ ').replace(
                    ' <!----></li><li class="table-row active">', '\n')
            text.replace(' <!----></li></ul>', '')
            await msg.edit(text)

        if message.chat.id in [-1001659763460, 1659763460, 1685499596, -1001685499596]:
            await message.client.send_message(121020442, message)
            stream = os.popen('node /home/pi/misc-files/make-screenshot.js')
            output = stream.read()
            await message.client.send_message(121020442, output)
            chats_data = self.db.get("SirenaInfo", "chats", [])
            for chat_id in chats_data:
                await message.client.send_message(121020442, f"Отправляю сообщение в чат {chat_id}")
                await message.client.send_file(chat_id, file='/home/pi/misc-files/webshot.jpg', caption=message.message)

        if message.chat_id in [1766138888, -1001766138888]:
            await message.client.send_message(121020442, message)
