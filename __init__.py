import os
import json
import dotenv
import random
import discord
import requests

from datetime import datetime
from discord.utils import get



bot_info = """Hey there! I'm Albus, a featured bot for this server.
You can use '$help' command to view all the available commands.

If you're new to discord bots/discord applications, I got you.

I have some link which you can visit and make your own Discord bot/application.

Check the footer message for the links
"""

resources_link = "https://discord.com/channels/1017808927691382824/1017808928416989311/1027161718427766844"
portal_link = f"https://discord.com/developers/applications"
discordPy_docs_link = "https://discordpy.readthedocs.io/en/latest/index.html"
wizard_link = "https://docs.google.com/presentation/d/1YiRKyaQjjEq5681G0D_IUc2dTOs0dH_C8hBkdyRJg7A/edit?usp=sharing"

bot_info_foot = f"""• [Discord Developer Portal]({portal_link})
• [Python Libraries You need]({resources_link})
• [Discord.py Library Docs]({discordPy_docs_link}) 
• [Wizard to make your own Discord application]({wizard_link}) 
"""


def cls():
    os.system('cls')


def get_cmd_info(prefix: str, key_to_get: str):
    random_prefix = random.choice(['!', '.', '/', '*', '&'])

    help = f"""This command works in two way:- 
1. If you just type $help, it will show you the list of all commands and the active prefic symbol.
2. If you type $help <command>, if will show you the info of that specified command.

For Ex:- $help or $help {prefix}ping"""

    info = """This command tells you about the bot. And the active command prefix of the bot. 
And provides you resources through which you can make your wown bot"""

    ping = "This command will show you the latency/ping of the bot host network."

    prefix_ = f"""This command helps you to change the active prefix of the bot command. 
You just have to type {prefix}prefix <new_prefix>. The prefix will be updated that moment.

For Ex:- {prefix}prefix {random_prefix}

Note:- Don't assign '@', '#', '$' as prefix"""

    verify = f"""When you join the server, you join as NewCommer and you can't view all the 
channels. To view the general channels you have to verify yourself.

Command Syntax:- {prefix}verify <your github username>
For Ex:- {prefix}verify abc
"""

    dev = f"""This command will give you the developer role. If you're verified and want to be 
a developer of this server. Then use this command to get the developer role.

Note:- Only members who have >=3 repo in their GitHub profile can get this role.
"""

    cmd_details = {
        '$help': help, 
        f'{prefix}info': info, 
        f'{prefix}ping': ping, 
        f'{prefix}dev': dev,
        f'{prefix}prefix': prefix_, 
        f'{prefix}verify': verify 
        }

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


def verify_member(github_username: str):
    details_api_url = f"https://api.github.com/users/{github_username}"
    user_data = json.loads(requests.get(details_api_url).content)

    if ('https://github.com/' in user_data["html_url"]) and \
        (int(user_data["public_repos"]) >= 1):
            return (True, str(user_data["name"]))

    elif int(user_data["public_repos"]) == 0:
        return (False, "To get verified you should have atleast 1 public repo.")

    else:
        return (False, "Invalid username. Enter a valid GitHub username")


def filter_data(data):
    filtered_data = []
    for member in data: filtered_data.append(str(member[0]))

    return filtered_data


def get_role(ctx, role_name: str):
    member = ctx.author
    role = get(member.guild.roles, name=role_name)

    return (member, role)