import threading
from urllib.parse import urlparse

from discord_bot.commands.base_command import BaseCommand
from video_search.find_vid import find_vid


class VideoSearchCommand(BaseCommand):
    """
    Reverse video search using an image
    The video search command is not invoked by messages with a certain prefix.
    It is invoked by uploading an image to designated channels.
    """

    COMMAND_OPTION = 'video'

    def __init__(self, client, config):
        """
        :param client: discord client
        :param config: configparser
        """

        self.client = client
        self.config = config[self.COMMAND_OPTION]
        channel_ids_str = self.config['channel_ids']
        # channel ids are integers
        self.allowed_channel_ids = [int(s) for s in channel_ids_str.split(',')]
        extensions_str = self.config['extensions']
        self.allowed_extensions = extensions_str.split(",")
        self.model_version = self.config['model_version']
        self.resolution = (int(self.config['resolution_x']), int(self.config['resolution_y']))
        self.topn = int(self.config['topn'])

    def get_command_prefix(self):
        return '上传图片到频道'

    def get_help_message(self):
        return '根据图片搜索视频'

    def execute(self, original_message):
        # TODO: the if block below is only checking images sent by uploading attachments,
        #  it will not work if the image is sent by directly posting a URL
        if original_message.attachments:
            url = original_message.attachments[0].url
            extension = self.get_extension_from_url(url)
            if extension in self.allowed_extensions:
                thread = threading.Thread(target=self.search, args=(original_message,))
                thread.start()

    def search(self, original_message):
        url = original_message.attachments[0].url
        result = find_vid(pic_path=url, resolution=self.resolution, topN=self.topn, pic_path_is_url=True)
        self.client.loop.create_task(original_message.reply(result, mention_author=True))

    def get_allowed_channel_ids(self):
        return self.allowed_channel_ids

    def get_extension_from_url(self, url):
        """
        get the file extension from a URL. e.g. jpg, png
        """

        path = urlparse(url).path
        path_components = path.split('.')
        if len(path_components) >= 2:
            return path_components[-1]
        else:
            return ''
