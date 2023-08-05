import logging
from typing import Optional

from redbot.core.commands import Cog, Context


class BaseCog(Cog):
    """
    Base cog for all other cogs to inherit from.
    """
    __author__ = "nwithan8"

    def __init__(self, name: str, bot):
        super().__init__()
        self.bot = bot

        log = logging.getLogger(f"red.cog.{name}")

    async def send_error(self, ctx: Context, error_message: Optional[str] = None):
        await ctx.send(error_message or "Something went wrong!")
