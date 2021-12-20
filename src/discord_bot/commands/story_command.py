import json
import threading

import requests

from discord_bot.commands.base_command import BaseCommand


class StoryCommand(BaseCommand):
    """
    Fetch a random story from an API
    """

    COMMAND_OPTION = 'story'

    def __init__(self, client, config):
        """
        :param client: discord client
        :param config: configparser
        """

        self.client = client
        self.config = config[self.COMMAND_OPTION]
        self.api_url = self.config['api_url']

    def get_command_prefix(self):
        return self.COMMAND_PREFIX + ' ' + self.COMMAND_OPTION

    def get_help_message(self):
        return '随机从Spanking Wiki中抽取一篇小说'

    def execute(self, original_message):
        thread = threading.Thread(target=self.request, args=(original_message,))
        thread.start()

    def request(self, original_message):
        response = requests.get(self.api_url)
        post = json.loads(response.text)
        embed = self.build_embed()

        # thumbnail
        embed.set_thumbnail(url=post["yoast_head_json"]["og_image"][0]["url"])
        # author, tags, and categories
        categories = []
        author = ""
        tags = []
        schemas = post["yoast_head_json"]["schema"]["@graph"]
        for schema in schemas:
            if schema["@type"] == "Article":
                categories = schema["articleSection"]
                tags = schema["keywords"]
            if schema["@type"] == "Person":
                author = schema["name"]
        embed.add_field(name="**发布者**", value=author, inline=True)
        embed.add_field(name="**分类**", value=" | ".join(categories), inline=True)
        embed.add_field(name="**标签**", value=", ".join(tags), inline=False)
        # CTA link
        read_link = "[**" + post["title"]["rendered"] + "**](" + post["link"] + ")"
        embed.add_field(name="**阅读全文**", value=read_link, inline=False)
        # footer
        embed.set_footer(text="Bot " + self.BOT_VERSION, icon_url="")

        self.client.loop.create_task(original_message.channel.send(embed=embed))
