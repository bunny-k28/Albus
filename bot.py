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



if __name__ == '__main__':
    

    @bot.event
    async def on_ready():
        print('Albus#2627 is online...\n\nLogs:-')


    @bot.event
    async def on_message(txt):
        message = str(txt.content)
        author = str(txt.author)
        channel = txt.channel

        OWNER_ID = os.getenv('OWNER_ID')
        prefix = os.getenv('PREFIX')

        flash_cmd(message, author)

        if txt.author == bot.user:
            pass
        
        if message == f'{prefix}info':
            await channel.send("**`Hey there! I'm Albus, a featured bot for this server.`**")

        elif message == f'{prefix}ping':

            ping = str(round(bot.latency, 2))
            await channel.send(f"**`Ping: {ping}`**")

        elif message.startswith(f'{prefix}prefix'):
            new_prefix = message.split(' ')[-1]
            msg_link = txt.jump_url

            try: 
                dotenv.set_key('Database/SECRETS.env', 'PREFIX', new_prefix)
                await channel.send(f'prefix updated to **`{new_prefix}`**')

            except Exception as E:
                issue_channel = bot.get_channel(1027193550007435334)
                await issue_channel.send(f'error in **`{prefix}prefix`** command\nmessage link:- {msg_link}')

        elif message == '$reboot$':

            if author == OWNER_ID:
                botID = str(bot.user)
                await channel.send(f'**`{botID} Will be updated within 5 to 7 seconds...`**')

                os.system(r'py .\bot.py')

            else:
                await channel.send(f"**`User {author} don't have the permissions to reboot the bot`**")

        elif message == '$shutdown$':
            if author == OWNER_ID: quit()
            else: await channel.send(f"**`User {author} don't have the permissions to reboot the bot`**")


    bot.run(BOT_TOKEN)