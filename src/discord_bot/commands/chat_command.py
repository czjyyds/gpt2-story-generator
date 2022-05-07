import threading
from collections import deque

from discord_bot.commands.base_command import BaseCommand
from generation.sanitization import *


class ChatCommand(BaseCommand):
    """
    A simple chat bot that responds to messages in a designated channel
    """

    COMMAND_OPTION = 'chat'

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
        channel_ids_str = self.config['channel_ids']
        # channel ids are integers
        self.allowed_channel_ids = [int(s) for s in channel_ids_str.split(',')]

        # fix length queue to track the chat history
        self.queue = deque([], maxlen=10)

    def get_command_prefix(self):
        return self.COMMAND_PREFIX + ' ' + self.COMMAND_OPTION

    def get_help_message(self):
        return '接龙游戏'

    def execute(self, original_message):
        """
        execute generation
        :param original_message: discord message object
        :return:
        """
        thread = threading.Thread(target=self.generate, args=(original_message,))
        thread.start()

    def get_allowed_channel_ids(self):
        return self.allowed_channel_ids

    def generate(self, original_message):
        # restart a new session
        if 'restart' == original_message.content:
            self.client.loop.create_task(original_message.channel.send('restarted'))
            self.queue = deque([], maxlen=10)
            return

        # rewrite the last generation
        elif 'rewrite' == original_message.content:
            self.client.loop.create_task(original_message.channel.send('rewriting...'))
            # remove the last generation from the queue
            self.queue.pop()

        else:
            message = self.get_prefix(original_message)
            message = message.strip()
            message = self.sanitize(message)
            message = self.finish_sentence_with_punctuation(message)

            # if user input is too long or too short
            if len(message) > self.max_length:
                self.client.loop.create_task(original_message.channel.send('不能超过800字'))
                return
            if len(message) < self.min_length:
                self.client.loop.create_task(original_message.channel.send('要10个字以上'))
                return

            # queue the message
            self.queue.append(message)

        # concatenate all the previously queued message
        history = ''.join(self.queue)

        # generation logic
        generated = self.model.generate(history)
        generated = self.remove_incomplete_sentence(generated)

        # queue the generated message
        self.queue.append(generated)

        # send result back
        self.client.loop.create_task(original_message.channel.send(generated))

    def finish_sentence_with_punctuation(self, sentence):
        """
        add period to the end of the sentence
        :param sentence:
        :return:
        """
        punctuation = ['。', '！', '？', '!', '?']
        has_tailing_punctuation = list(filter(sentence.endswith, punctuation)) != []
        # if a valid punctuation is missing at the end of the sentence
        if not has_tailing_punctuation:
            sentence = sentence + '。'
        return sentence

    def remove_incomplete_sentence(self, sentence):
        """
        remove the dangling/incomplete part from the end of the sentence
        e.g. 夜正长，路也正长，我们忘却了 ==> 夜正长，路也正长，
        :param sentence:
        :return:
        """
        punctuation = ['。', '，', '！', '？', ',', '!', '?']
        # tracks the position of the last punctuation
        last_punctuation = len(sentence)
        for i in range(0, len(sentence)):
            if sentence[i] in punctuation:
                last_punctuation = i
        return sentence[0:last_punctuation + 1]

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
