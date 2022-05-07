import threading
import time

from discord_bot.commands.base_command import BaseCommand
from generation.sanitization import *


class WriteCommand(BaseCommand):
    """
    Generate text based on a prefix provided
    """

    COMMAND_OPTION = 'write'

    def __init__(self, client, config, model):
        """
        :param client: discord client
        :param config: configparser
        :param model: generation model
        """
        self.client = client
        self.model = model
        self.config = config[self.COMMAND_OPTION]
        self.max_length = int(self.config['max_length'])
        self.min_length = int(self.config['min_length'])
        self.model_version = self.config['model_version']

    def get_command_prefix(self):
        return self.COMMAND_PREFIX + ' ' + self.COMMAND_OPTION

    def get_help_message(self):
        return '根据提供prefix续写'

    def execute(self, original_message):
        """
        execute generation
        :param original_message: discord message object
        :return:
        """
        thread = threading.Thread(target=self.generate, args=(original_message,))
        thread.start()

    def generate(self, original_message):
        prefix = self.get_prefix(original_message)
        prefix = prefix.strip()
        prefix = self.sanitize(prefix)

        # if prefix is too long or too short
        if len(prefix) > self.max_length:
            embed = self.build_embed("文太长了...不能超过800字")
            self.client.loop.create_task(original_message.channel.send(embed=embed))
            return
        if len(prefix) < self.min_length:
            embed = self.build_embed("文太短了...要30个字以上")
            self.client.loop.create_task(original_message.channel.send(embed=embed))
            return

        start_time = time.time()
        # the hash value of the concatenation of the prefix and the current timestamp
        generation_id = str(hash(prefix + str(start_time)))

        # send back the first embed, which includes the prefix the user has provided
        embed = self.build_embed("正在根据Prefix续写中...预计需要2-3分钟...")
        embed.add_field(name="**Prefix:**", value=prefix, inline=False)
        embed.set_footer(
            text="Bot " + self.BOT_VERSION + "   |   Model " + self.model_version + "   |   ID " + generation_id,
            icon_url=""
        )
        self.client.loop.create_task(original_message.channel.send(embed=embed))

        # generation logic
        generated = self.model.generate(prefix)

        # send the second embed, which includes the generated text
        time_elapsed = str(round(time.time() - start_time, 2))
        embed = self.build_embed("续写完成")
        embed.add_field(name="**结果:**", value=generated, inline=False)
        embed.set_footer(
            text="Bot " + self.BOT_VERSION + "   |   Model " + self.model_version + "   |   Time elapsed "
            + time_elapsed + "   |   ID " + generation_id,
            icon_url=""
        )
        self.client.loop.create_task(original_message.channel.send(embed=embed))

    def get_prefix(self, original_message):
        return original_message.content.replace(self.get_command_prefix(), '')

    def sanitize(self, prefix):
        prefix = ''.join(prefix.split())
        prefix = prefix.lower()
        # sanitize prefix
        prefix = remove_discord_emojis(prefix)
        prefix = unescape_html(prefix)
        prefix = remove_special_characters(prefix)
        prefix = remove_html_xml_tags(prefix)
        prefix = remove_urls(prefix)
        prefix = convert_and_remove_punctuation(prefix)
        prefix = remove_nonchinese_characters(prefix)
        return prefix
