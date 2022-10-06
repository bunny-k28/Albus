"""
BOT - Albus#2627
"""

import os
import dotenv
import discord
import termcolor

from __init__ import *


cls()
dotenv.load_dotenv('Database/SECRETS.env')

print(f"ACTION: preparing {termcolor.colored('Albus#2627', color='yellow')}... STATUS: ", end='')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = discord.Client(intents=intents)
termcolor.cprint('Ready', 'green')

prefix_ = ''



if __name__ == '__main__':
    

    @bot.event
    async def on_ready():
        print('Albus#2627 is online...\n\nLogs:-')


    @bot.event
    async def on_message(txt):
        global prefix_

        message = str(txt.content)
        author = str(txt.author)
        channel = txt.channel

        OWNER_ID = os.getenv('OWNER_ID')
        prefix = prefix_ = dotenv.get_key('Database/SECRETS.env', 'PREFIX')

        flash_cmd(message, author)

        if txt.author == bot.user:
            pass

        # help command
        if message.startswith('$help'):
            try: 
                cmd = message.split(' ')
                cmd.remove('$help')

            except IndexError: pass

            if cmd.__len__() >= 1:
                try: 
                    cmd_info = get_cmd_info(prefix, cmd[-1])
                    await channel.send(f'Command: **`{cmd}`**\nInfo:- **```{cmd_info}```**')

                except IndexError as IE: print("error in help commannd", IE)

            else:
                with open('Database/commands.txt', 'r') as cmd_file:
                    cmds = cmd_file.read()

                await channel.send(f"Active Prefix Symbol:- ``{prefix}``\n{cmds}")

        # info command
        elif message == f'{prefix}info':
            await channel.send(f"**`Hey there! I'm Albus, a featured bot for this server.`**")

        # ping command
        elif message == f'{prefix}ping':

            ping = str(int(round(bot.latency, 2) * 100))
            await channel.send(f"**`Ping: {ping}ms`**")

        # prefix change command
        elif message.startswith(f'{prefix}prefix'):
            new_prefix = message.split(' ')[-1]
            msg_link = txt.jump_url

            try: 
                change_status = dotenv.set_key('Database/SECRETS.env', 'PREFIX', new_prefix)
                await channel.send(f'prefix updated to **`{new_prefix}`**')

            except Exception as E:
                issue_channel = bot.get_channel(1027193550007435334)
                await issue_channel.send(f'error in **`{prefix}prefix`** command\nmessage link:- {msg_link}')

        # bot reboot command (only for dev use)
        elif message == '$reboot$':

            if author == OWNER_ID:
                botID = str(bot.user)
                await channel.send(f'**`{botID} Will be updated within 5 to 7 seconds...`**')

                os.system(r'py .\bot.py')

            else:
                await channel.send(f"**`User {author} don't have the permissions to reboot the bot`**")

        # bot shutdown command
        elif message == '$shutdown$':
            if author == OWNER_ID: quit()
            else: await channel.send(f"**`User {author} don't have the permissions to reboot the bot`**")


    bot.run(BOT_TOKEN)