import os
import dotenv
import random
import discord

from datetime import datetime


def cls():
    os.system('cls')


def get_cmd_info(prefix: str, key_to_get: str):
    random_prefix = random.choice(['!', '.', '/', '*', '&'])

    help = f"""This command works in two way:- 
1. If you just type $help, it will show you the list of all commands and the active prefic symbol.
2. If you type $help <command>, if will show you the info of that specified command.

For Ex:- $help or $help {prefix}ping"""

    info = "This command tells you about the bot. And the active command prefix of the bot."

    ping = "This command will show you the latency/ping of the bot host network."

    prefix_ = f"""This command helps you to change the active prefix of the bot command. 
You just have to type {prefix}prefix <new_prefix>. The prefix will be updated that moment.

For Ex:- {prefix}prefix {random_prefix}

Note:- Don't assign '@', '#', '$' as prefix"""

    cmd_details = {
        '$help': help, 
        f'{prefix}info': info, 
        f'{prefix}ping': ping, 
        f'{prefix}prefix': prefix_}

    return cmd_details[key_to_get]


def flash_cmd(command: str, author: str):
    prefix = dotenv.get_key(dotenv_path='Database/SECRETS.env', key_to_get='PREFIX')

    date = str(datetime.now().strftime('%d-%h-%y'))
    time = str(datetime.now().time())[:5]

    if author == 'Albus#2627': pass
    elif ((author != 'Albus#2627') and (command.startswith(prefix)) or (command.startswith('$'))): 
        with open('Database/cmd_logs.txt', 'a', encoding='utf-8') as cmd_logs:
            cmd_logs.write(f'{date} ~ {time}\n•Command used: {command}\n•By: {author}\n\n')

        print(f"Command used: {command}\nBy: {author}\n")


def embed(color: discord.Colour, cmd: str, message: str, title: str='', footer: str=''):
    embed_msg = discord.Embed(
        colour=color, 
        title=f'Command: **`{cmd}`**\n{title}', 
        description=f'**```{message}```**\n\n{footer}'
    )

    return embed_msg