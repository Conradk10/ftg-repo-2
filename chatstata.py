import datetime
import random
import collections
from asyncio import sleep
from telethon import types
from rich import print

from .. import loader, utils


@loader.tds
class ChatStataMod(loader.Module):
    """Модуль статистики чата"""
    strings = {
        'name': 'ChatStata',
        'pref': '<b>[ChatStata]</b> '
    }
    db_name = 'ChatStata'

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def chatstatacmd(self, message: types.Message):
        """Просмотр статистики чата"""
        client = self.client
        await utils.answer(message, "<b>📊 Подсчитываем топ по количеству сообщений...</b>")
        chat = message.input_chat
        out = {}
        async for i in client.iter_participants(message.chat_id):
            if not i.deleted:
                count = (await client.get_messages(chat, from_user=i.id)).total
                name = str(str(i.first_name) + (" " + i.last_name if i.last_name else ""))
                if count > 3:
                    out[count] = "<b>" + str(name) + "</b>"

        od = dict(collections.OrderedDict(sorted(out.items(), reverse=True)))
        out = ["<b>📊 Топ по количеству сообщений:</b>\n"]
        for count, user in od.items():
            out.append(user + ": " + str(count))

        await utils.answer(message, "\n".join(out))
