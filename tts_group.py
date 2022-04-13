# -*- coding: utf-8 -*-
from gtts import gTTS
from io import BytesIO
from .. import loader, utils


@loader.tds
class GroupTTSMod(loader.Module):
    """Тест в речь для групп"""
    strings = {"name": "GroupTTS",
               "tts_lang_cfg": "<b>[TTS]</b> Установите код языка для преобразования в речь здесь.",
               "tts_needs_text": "<b>[TTS]</b> Мне нужен текст для преобразования в речь!",
               "tts_loading": "<b>[TTS]</b> Начинаю преобразование текста в речь. Это может занять немного времени."}

    def __init__(self):
        self.config = loader.ModuleConfig("TTS_LANG", "ru", lambda m: self.strings("tts_lang_cfg", m))

    async def watcher(self, message):
        """Преобразование текста в речь с помощью API Google"""
        if message.text.lower() in ['/tts']:
            text = utils.get_args_raw(message.message)
            if len(text) == 0:
                if message.is_reply:
                    text = (await message.get_reply_message()).message
                    message = await utils.answer(message, self.strings("tts_loading", message))
                else:
                    await utils.answer(message, self.strings("tts_needs_text", message))
                    return

            tts = await utils.run_sync(gTTS, text, lang=self.config["TTS_LANG"])
            voice = BytesIO()
            await utils.run_sync(tts.write_to_fp, voice)
            voice.seek(0)
            voice.name = "voice.mp3"

            await utils.answer(message, voice, voice_note=True)
