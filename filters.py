from config import ADMINS

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from dbAPI import getChannels

class IsAdminFilter(BoundFilter):
    key = 'isAdminFilter'

    def __init__(self, isAdminFilter) -> None:
        self.isAdminFilter = isAdminFilter

    async def check(self, message: Message) -> bool:
        return message.from_user.id in ADMINS

