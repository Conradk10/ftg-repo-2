# -*- coding: utf-8 -*-
import os
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

        return await message.edit("<b>[Sirena Info]</b> Ни один аргумент не выбран!")

    async def watcher(self, message):
        if message.chat_id in [-1001659763460, -1001685499596]:
            stream = os.popen('node /home/pi/misc-files/make-screenshot.js')
            output = stream.read()
            print(output)

            chats_data = self.db.get("SirenaInfo", "chats", [])

            for chat_id in chats_data:
                await message.client.send_file(chat_id, file='/home/pi/misc-files/webshot.png', caption=message.message)
