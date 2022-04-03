# -*- coding: utf-8 -*-
from .. import loader, utils
import io
import requests
import datetime


@loader.tds
class SirenaInfoMod(loader.Module):
    """Информирование о сиренах в Днепре"""
    strings = {'name': 'SirenaInfo'}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    async def sinfocmd(self, message):
        """Включить/выключить оповещение сирены.
        Используй:
        .sirenainfo <clearall>
        .sirenainfo <listall>
        .sirenainfo <on>
        .sirenainfo <off> """

        chats_data = self.db.get("SirenaInfo", "chats", [])

        chat_id = message.chat_id
        args = utils.get_args_raw(message)
        if args == "clearall":
            self.db.set("SirenaInfo", "chats", [])
            return await message.edit("<b>[Sirena Info]</b> Все настройки чатов сброшены")

        elif args == "listall":
            return await message.edit(f"<b>[Sirena Info]</b> Все чаты в базе данных:\n{chats_data}")

        elif args == "on":
            if chat_id in chats_data:
                return await message.edit(f"<b>[Sirena Info]</b> Чат уже был добавлен!\n\n"
                                          f"Все чаты в базе данных:\n{chats_data}")
            else:
                chats_data.append(chat_id)
                self.db.set("SirenaInfo", "chats", chats_data)
                return await message.edit(f"<b>[Sirena Info]</b> Чат добавлен успешно!\n\n"
                                          f"Все чаты в базе данных:\n{chats_data}")

        elif args == "off":
            if chat_id in chats_data:
                chats_data.pop(chat_id)
                self.db.set("SirenaInfo", "chats", chats_data)
                return await message.edit(f"<b>[Sirena Info]</b> Чат успешно удален!\n\n"
                                          f"Все чаты в базе данных:\n{chats_data}")
            else:
                return await message.edit(f"<b>[Sirena Info]</b> Чат уже был удален!\n\n"
                                          f"Все чаты в базе данных:\n{chats_data}")

        return await message.edit("<b>[Sirena Info]</b> Ни один аргумент не выбран!")

    async def watcher(self, message):
        """Интересно, почему он именно watcher называется... 🤔"""
        if message.chat_id in [-1001659763460, -1001685499596]:
        # if message.chat_id == 121020442:
            chats_data = self.db.get("SirenaInfo", "chats", [])
            # chats_data = [121020442,]
            file = requests.get(
                "https://shot.screenshotapi.net/screenshot?&url=https%3A%2F%2Fwar.ukrzen.in.ua%2Falerts%2F%3F" + str(
                    datetime.datetime.now().timestamp()) + "&width=1400&height=1000&output=image&file_type=png&wait_for_event=load")
            file = io.BytesIO(file.content)
            file.name = "webshot.png"
            file.seek(0)
            print(message.text)

            for chat_id in chats_data:
                await message.client.send_file(chat_id, file, caption=message.message)
                print('Отправлено сообщение о тревоге')
