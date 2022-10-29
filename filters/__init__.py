from telegram.ext import Filters, MessageFilter
from telegram import Message

class text(MessageFilter):
    def filter(self, message:Message):
        return message.text is not None and message.caption is not None

class button(MessageFilter):
    def __init__(self, btn_text):
        self.btn_text = btn_text

    def filter(self, message: Message):
        if message.text is None:
            return False
        if isinstance(self.btn_text, str):
            return self.btn_text == message.text
        if isinstance(self.btn_text, list):
            return message.text in self.btn_text

class artwork(MessageFilter):
    def filter(self, message: Message):
        return message.photo is not None or \
                message.audio is not None or \
                message.video is not None
