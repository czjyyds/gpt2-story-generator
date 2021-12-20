from abc import ABC, abstractmethod

import discord


class BaseCommand(ABC):

    BOT_VERSION = "v0.3"
    COMMAND_PREFIX = "$wiki"
    EMBED_TITLE = "中文SP资料库 Spanking Wiki"
    EMBED_TITLE_URL = "https://spanking.wiki/"
    EMBED_FOOTER = "中文SP资料库 Spanking Wiki"
    EMBED_COLOR = 0xa03311

    def build_embed(self,  description=""):
        """
        description is optional,
        embed footer is not set by this function, use set_footer on the embed returned to set your own footer.
        https://discordpy.readthedocs.io/en/stable/api.html#embed
        :param description: the description of the embed
        :return: a Discord embed
        """
        return discord.Embed(
            title=self.EMBED_TITLE,
            url=self.EMBED_TITLE_URL,
            description=description,
            footer=self.EMBED_FOOTER,
            color=self.EMBED_COLOR
        )

    @abstractmethod
    def get_command_prefix(self):
        """
        :return: the command prefix that the message content must start with to invoke this command.
        """
        pass

    @abstractmethod
    def get_help_message(self):
        """
        :return: the help message for this command.
        """
        pass

    @abstractmethod
    def execute(self):
        pass
