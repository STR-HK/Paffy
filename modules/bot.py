from modules import permissions
from discord.ext.commands import AutoShardedBot


class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        """
        메시지를 보낼 권한이 있는지 확인.
        """
        super().__init__(*args, **kwargs)

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
            return

        await self.process_commands(msg)