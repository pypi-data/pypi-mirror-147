class Message:
    def __init__(self, message, bot):
        self.author = message['username']
        self.content = message['message']
        self.bot = bot

    async def reply(self, content):
        await self.bot.send(f"Replying to @{self.author} ({self.content}): {content}")