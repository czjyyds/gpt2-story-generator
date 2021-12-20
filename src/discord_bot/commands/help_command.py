import threading

from discord_bot.commands.base_command import BaseCommand


class HelpCommand(BaseCommand):
    """
    The help command should be invoked when command option is missing or invalid.
    It will send an embed that displays short descriptions of the available commands.
    """

    def __init__(self, client, commands):
        self.client = client
        self.commands = commands

    def get_command_prefix(self):
        return self.COMMAND_PREFIX

    def get_help_message(self):
        return ''

    def execute(self, original_message):
        thread = threading.Thread(target=self.send_help_message, args=(original_message,))
        thread.start()

    def send_help_message(self, original_message):
        """
        send an embed that displays short descriptions of the available commands.
        :param original_message:
        :return:
        """

        embed = self.build_embed()
        for command in self.commands:
            embed.add_field(name='**' + command.get_command_prefix() + '**',
                            value=command.get_help_message(), inline=False)
        embed.set_footer(text="Bot " + self.BOT_VERSION, icon_url="")
        self.client.loop.create_task(original_message.channel.send(embed=embed))
