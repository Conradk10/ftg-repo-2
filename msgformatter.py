import datetime
import random
from asyncio import sleep
from telethon import types
from rich import print

from .. import loader, utils


@loader.tds
class ChatFormatterMod(loader.Module):
    """Модуль который автоматом форматирует отправленные сообщения.
    Подставляет текст перед и после вашего сообщения"""
    strings = {
        'name': 'ChatFormatter',
        'pref': '<b>[ChatFormatter]</b> '
    }
    db_name = 'ChatFormatter'

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def cfprefixcmd(self, m: types.Message):
        """Устанавливает префикс"""
        self.db.set(self.db_name, 'prefix', utils.get_args_raw(m))
        await utils.answer(m, f'{self.strings["pref"]} Установлен префикс: <code>{utils.get_args_raw(m)}</code>')


    async def cfsuffixcmd(self, m: types.Message):
        """Устанавливает суффикс"""
        self.db.set(self.db_name, 'suffix', utils.get_args_raw(m))
        await utils.answer(m, f'{self.strings["pref"]} Установлен суффикс: <code>{utils.get_args_raw(m)}</code>')


    async def cftogglecmd(self, m: types.Message):
        """Вкл/выкл форматирование сообщений"""
        if self.db.get(self.db_name, 'toggle', []) != "True":
            self.db.set(self.db_name, 'toggle', "True")
        else:
            self.db.set(self.db_name, 'toggle', "False")

        await utils.answer(m, f'{self.strings["pref"]} Сейчас модуль: '
                              f'<code>{self.db.get(self.db_name, "toggle", [])}</code>')


    async def cfstatuscmd(self, m: types.Message):
        """Просмотр настроек"""
        await utils.answer(m, f'{self.strings["pref"]} '
                              f'Сейчас модуль: <code>{self.db.get(self.db_name, "toggle", [])}</code>\n'
                              f'Префикс: <code>{self.db.get(self.db_name, "prefix", [])}</code>\n'
                              f'Суффикс: <code>{self.db.get(self.db_name, "suffix", [])}</code>')


    async def watcher(self, m: types.Message):
        if self.db.get(self.db_name, 'toggle', []) != "True":
            return

        if m.raw_text.startswith("."):
            return

        if m.raw_text == "":
            return

        if m.sender_id == 121020442:
            await m.edit(self.db.get(self.db_name, 'prefix', [])
                         + m.raw_text +
                         self.db.get(self.db_name, 'suffix', []))
        return
