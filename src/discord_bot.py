import configparser

import discord

from discord_bot.commands.help_command import HelpCommand
from discord_bot.commands.story_command import StoryCommand
from discord_bot.commands.video_search_command import VideoSearchCommand
from discord_bot.commands.write_command import WriteCommand
from discord_bot.commands.chat_command import ChatCommand
from discord_bot.keep_alive import keep_alive

from generation.generate import Generate

client = discord.Client()
generate = Generate()
# load discord bot configs
config = configparser.ConfigParser()
config.read('config.ini')
discord_config = config['discord']
debug_mode = discord_config.getboolean('debug')
game_playing_status = discord_config['game_playing_status']

# prepare command handlers
write_command = WriteCommand(client, config, generate)
story_command = StoryCommand(client, config)
video_search_command = VideoSearchCommand(client, config)
chat_command = ChatCommand(client, config, generate)

available_commands = [write_command, story_command, video_search_command]
help_command = HelpCommand(client, available_commands)


# bot ready event handler
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    if debug_mode:
        print('DEBUG MODE ENABLED')
    # set bot status
    await client.change_presence(activity=discord.Game(game_playing_status))


# message event handler
@client.event
async def on_message(message):
    # if the message is from the bot itself, skip it
    if message.author == client.user:
        return

    # if bot is set to debug mode,
    # and the message is not from one of the debug channels defined in the config file, skip it
    if debug_mode:
        # channel ids are integers
        debug_channel_ids = [int(s) for s in discord_config['debug_channel_ids'].split(',')]
        if message.channel.id not in debug_channel_ids:
            return

    # video search command
    # if the message is from the designated channel for video searching
    if message.channel.id in video_search_command.get_allowed_channel_ids():
        video_search_command.execute(message)

    # story command
    if message.content.startswith(story_command.get_command_prefix()):
        story_command.execute(message)

    # write command
    elif message.content.startswith(write_command.get_command_prefix()):
        write_command.execute(message)

    # message was sent in the chat channels
    elif message.channel.id in chat_command.get_allowed_channel_ids():
        chat_command.execute(message)

    # display the help message
    elif message.content.startswith(help_command.get_command_prefix()):
        help_command.execute(message)

keep_alive()

client.run(discord_config['key'])
