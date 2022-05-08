"""
Copyright 2022 t.me/ca4tuk
Licensed under the Creative Commons CC BY-NC-ND 4.0

Full license text can be found at:
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Human-friendly one:
https://creativecommons.org/licenses/by-nc-nd/4.0
"""

import requests
import random

import html

from .. import loader, utils, inline
from pyrogram import Client, types

from aiogram.types import (
    InlineQuery,
    CallbackQuery,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto
)

@loader.module(name="ToxicKid", author="ca4tuk", version=13.37)
class txckdMod(loader.Module):
    """<b>Я, твоего деда, нахуй, на хуй посадил</b>"""

    strings = {
        "loh": "💢 Тебе такое нельзя, вступай в ряды!",
        "waiting": "⏳ <b>Ждём ответа от бота</b>...",
        "not_a_chat": "💢 <b>Бездарь, команда разрешена только в публичный чатах</b>",
        "unknown_error": "🤷‍♂️ Возникла неожиданная ошибка"
    }

    async def check_chat(self, app: Client, chat_id):
        try:
            chat = await app.get_chat(chat_id)
        except Exception as err:
            return False
        chats = self.db.get("ToxicKid", "chats", {})
        if chat_id not in chats:
            chats.update({str(chat.id): {"work": True, "reaction_to_reply": True, "activity": 50}})
            self.db.set("ToxicKid", "chats", chats)
        return chat

    async def get_chat_info(self, app: Client, chat):
        chats = self.db.get("ToxicKid", "chats", {})
        data = chats.get(str(chat.id))
        text = (f"🗂 <b>Настройки чата</b>:\n{html.escape(chat.title)}\n\n"
                f"🖥 <b>{'Включено' if data['work'] else 'Выключено'}</b>\n"
                f"👁‍🗨 <b>Активность</b>: <i>{data['activity']}% из 100%</i>\n"
                f"💬 <b>Реакция на ответы</b>: <i>{'да' if data['reaction_to_reply'] else 'нет'}</i>\n")
        return text

    async def get_chat_settings_keyboard(self, app: Client, chat):
        chats = self.db.get("ToxicKid", "chats", {})
        data = chats.get(str(chat.id))
        kb = InlineKeyboardMarkup(row_width=1)
        kb.insert(InlineKeyboardButton(
            text=("✅ Включено" if data['work'] else "❌ Выключено"), callback_data=f"toxic chat_id:{chat.id} change:work")
        )
        kb.insert(InlineKeyboardButton(
            text=f"Активность в чате: {data['activity']}%", callback_data=f"toxic chat_id:{chat.id} change:activity")
        )
        kb.insert(InlineKeyboardButton(
            text=f"Реакция на ответы: {'да' if data['reaction_to_reply'] else 'нет'}", callback_data=f"toxic chat_id:{chat.id} change:reply")
        )
        return kb

    async def toxic_cmd(self, app: Client, message: types.Message):
        """Вызывает управлятор"""

        if message.chat.type not in ["group", "supergroup"]:
            return await utils.answer(
                message, self.strings["not_a_chat"])

        await utils.answer(
            message, self.strings["waiting"])
        bot_results = await app.get_inline_bot_results( # вызывает инлайн у бота
            (await self.inline.bot.me).username, f"toxic {message.chat.id}")
        await app.send_inline_bot_result( # тыкает на настройки
            message.chat.id, bot_results.query_id,
            bot_results.results[0].id
            )
        await message.delete()

    async def toxic_inline_handler(self, app: Client, inline_query: InlineQuery):
        """Дает управлятор"""

        prefix = self.db.get("sh1t-ub.loader", "prefixes", ["-"])[0]
        switch_pm_text=f"🤬 Токсичный ребенок v0.1"
        args = (inline_query.query).split()
        chat_id = None
        chat = None
        results = []
        try:
            chat_id = str(args[1])
        except (ValueError, IndexError) as err:
            pass
        if chat_id is None:
            switch_pm_text = f"😡 Бездарь, используй команду {prefix}toxic"
        else:
            chat = await self.check_chat(app, str(chat_id))
        if chat and chat.type in ["group", "supergroup"]:
            results.append(
                InlineQueryResultArticle(
                    id=inline.result_id(),
                    title="Настройки чата",
                    description=f"{chat.title}",
                    input_message_content=InputTextMessageContent(
                        await self.get_chat_info(app, chat)
                    ),
                    reply_markup=InlineKeyboardMarkup().add(
                        InlineKeyboardButton("⚙️ Настройки чата", callback_data=f"toxic chat_id:{chat.id} settings"))
                )
            )
        else:
            switch_pm_text = f"😡 Бездарь, используй команду {prefix}toxic"
        await inline_query.answer(
            results=results,
            cache_time=0,
            switch_pm_parameter="toxic",
            switch_pm_text=switch_pm_text,

        )

    async def toxic_callback_handler(self, app: Client, callback: CallbackQuery):
        """Срет"""

        args = (callback.data.split())
        if not args[0] == "toxic":
            return
        if int(callback.from_user.id) != int((await app.get_me()).id):
            return await callback.answer(
                        self.strings["loh"], show_alert = True)
        chats = self.db.get("ToxicKid", "chats", {})
        chat_id = None
        check = None
        action = None
        what = None
        for arg in args:
            if arg.startswith("chat_id"):
                chat_id = str(arg.split(':')[1])
                check = await self.check_chat(app, str(chat_id))

            elif arg.startswith("settings"):
                action = "settings"
    
            elif arg.startswith("change"):
                action = "change"
                what = arg.split(':')[1]

        if not check:
            return await callback.answer(
                self.strings["unknown_error"], show_alert = True)
        if action == "change":
            if what == "reply":
                chats[chat_id].update({"reaction_to_reply": (False if chats[str(chat_id)]["reaction_to_reply"] else True)})
                self.db.set("ToxicKid", "chats", chats)
            elif what == "activity":
                data = chats.get(str(chat_id))
                activity = int(data["activity"])
                activity += 10
                if activity > 100:
                    activity = 10
                chats[chat_id].update({"activity": activity})
            elif what == "work":
                chats[chat_id].update({"work": (False if chats[str(chat_id)]["work"] else True)})
            self.db.set("ToxicKid", "chats", chats)
        return await self.inline.bot.edit_message_text(
            inline_message_id=callback.inline_message_id,
            text=await self.get_chat_info(app, check),
            reply_markup=await self.get_chat_settings_keyboard(app, check)
        )

    @loader.on(lambda _, __, m: not m.outgoing and m.chat.type in ["group", "supergroup"])
    async def watcher_toxic(self, app: Client, message: types.Message):
        """Срет в чатик"""
        chat = message.chat

        chats = self.db.get("ToxicKid", "chats", {})
        if not (current_chat := chats.get(str(chat.id))):
            return

        if not chats.get(str(chat.id))["work"]:
            return

        chance = current_chat["activity"]
        if random.randint(0, 100) >= chance:
            return

        reply = message.reply_to_message
        if reply.outgoing:
            if not current_chat["reaction_to_reply"]:
                return

        try:
            curse = (requests.get("https://backend.z-net.xyz/generate_curse").json())["curse"][0]
            await message.reply(curse)
        except: 
            pass

