#
#     8888888888P       888b    888          888
#           d88P        8888b   888          888
#          d88P         88888b  888          888
#         d88P          888Y88b 888  .d88b.  888888
#        d88P           888 Y88b888 d8P  Y8b 888
#       d88P     888888 888  Y88888 88888888 888
#      d88P             888   Y8888 Y8b.     Y88b.
#     d8888888888       888    Y888  "Y8888   "Y888
#
#                  https://z-net.xyz
#
#             Licensed under the GNU GPLv3
#      https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://st3.depositphotos.com/1472772/17102/i/450/depositphotos_171023276-stock-photo-zipped-mouth-emoji-isolated-on.jpg?forcejpeg=true
# meta desc: SwMute
# meta developer: @reverserave

# scope: hikka_only


import logging
from telethon import types
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class SwMuteMod(loader.Module):
    """ Оригинальный способ закрыть рот пользователю.
    После попадания в мут - модуль будет удалять все сообщения жертвы.
    В группах требуются право на удаление сообщений!"""

    strings = {
        "name": "SwMute",
        "now_in_mute": "{} <b><a href='tg://user?id={}'>{}</a>, now you're muted.</b>",
        "alredy_now_in_mute": "{} <b>{} already muted.</b>",
        "now_not_in_mute": "{} <b><a href='tg://user?id={}'>{}</a>, now you're not muted.</b>",
        "alredy_not_in_mute": "{} <b>{} was not muted.</b>",
        "args_error": "{} <b>User <code>{}</code> not found.</b>",
        "muted_users_list": "📇 <b>Here is the list of muted users:</b>\n{}",
        "muted_users_list_empty": "📇 <b>The list of users in the mute is empty</b>",
        "_mute_emoji": "🚫",
        "_unmute_emoji": "☑️",
        "_info_emoji": "ℹ️"
    }

    strings_ru = {
        "now_in_mute": "{} <b><a href='tg://user?id={}'>{}</a>, теперь ты в муте.</b>",
        "alredy_now_in_mute": "{} <b>{} уже находится в муте.</b>",
        "now_not_in_mute": "{} <b><a href='tg://user?id={}'>{}</a>, теперь ты не в муте.</b>",
        "alredy_not_in_mute": "{} <b>{} не был в муте.</b>",
        "args_error": "{} <b>Пользователь <code>{}</code> не найден.</b>",
        "muted_users_list": "📇 <b>Вот список пользователей в муте:</b>\n{}",
        "muted_users_list_empty": "📇 <b>Список пользователей в муте пуст.</b>",
        "_mute_emoji": "🚫",
        "_unmute_emoji": "☑️",
        "_info_emoji": "ℹ️"
    }

    def __init__(self) -> None:
        self.config = loader.ModuleConfig(
            "custom_mute_emoji", "🚫", lambda: self.strings("_mute_emoji"),
            "custom_unmute_emoji", "☑️", lambda: self.strings("_unmute_emoji"),
            "custom_info_emoji", "ℹ️", lambda: self.strings("_info_emoji")
        )

    async def client_ready(self, client, db) -> None:
        self.db = db
        self.client = client
        self.muted_users = self.db.get("swmute", "muted_users", [])

    async def _get_entity(self, message: types.Message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        entity = None
        if reply and not args:
            entity = await self.client.get_entity(reply.sender_id)
        if args and not reply:
            args = args.split()
            if args[0].isnumeric():
                args[0] = int(args[0])
            try:
                entity = await self.client.get_entity(args[0])
            except (ValueError, AttributeError):
                await utils.answer(message, self.strings['args_error'].format(
                    self.config["custom_info_emoji"], args[0]))
        return entity

    async def swmutecmd(self, message: types.Message) -> None:
        """ swmute <@ или реплай> - замутить пользователя """
        entity = await self._get_entity(message)
        if entity and entity.id not in self.muted_users:
            self.muted_users.append(entity.id)
            self.db.set("swmute", "muted_users", self.muted_users)
            await utils.answer(message, self.strings['now_in_mute'].format(
                self.config['custom_mute_emoji'], entity.id, entity.first_name))
        elif entity and entity.id in self.muted_users:
            await utils.answer(message, self.strings['alredy_now_in_mute'].format(
                self.config['custom_mute_emoji'], entity.first_name))

    async def swunmutecmd(self, message: types.Message) -> None:
        """ swunmute <@ или реплай> - размутить пользователя """
        entity = await self._get_entity(message)
        if entity and entity.id in self.muted_users:
            self.muted_users.remove(entity.id)
            self.db.set("swmute", "muted_users", self.muted_users)
            await utils.answer(message, self.strings['now_not_in_mute'].format(
                self.config['custom_unmute_emoji'], entity.id, entity.first_name))
        elif entity and entity.id not in self.muted_users:
            await utils.answer(message, self.strings['alredy_not_in_mute'].format(
                self.config['custom_unmute_emoji'], entity.first_name))

    async def swlistcmd(self, message: types.Message) -> None:
        """ swlist - отображает список пользователей в муте """
        if not self.muted_users:
            await utils.answer(message, self.strings['muted_users_list_empty'])
            return
        users = []
        for i in range(len(self.muted_users)):
            entity = await self.client.get_entity(self.muted_users[i])
            users.append("<b>{}.</b> <a href='tg://user?id={}'>{}</a> ({})".format(
                i+1, entity.id, entity.first_name, entity.id))
        await utils.answer(message, self.strings['muted_users_list'].format("\n".join(users)))

    async def watcher(self, message: types.Message) -> None:
        if message.from_id in self.muted_users:
            try:
                await message.delete()
            except Exception as err:
                logger.error(err)
