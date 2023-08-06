from .message import Message
import time

class Context:
    def __init__(self, bot, message, cmd):
        self.bot = bot
        self.message = Message(message, bot)
        self.command = cmd
        self.time = time.strftime("%H:%M:%S", time.localtime())

    async def reply(self, content):
        await self.bot.send(f"Replying to @{self.message.author} ({self.message.content}): {content}")

    async def send(self, content):
        await self.bot.send(content)

    @property
    def is_owner(self):
        return self.message.author == self.bot.owner
    

    