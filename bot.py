"""
BOT - Albus#2627
"""

import os
import dotenv
import sqlite3
import discord
import termcolor

from discord import Colour
from __init__ import *


cls()
dotenv.load_dotenv('Database/SECRETS.env')

print(f"ACTION: preparing {termcolor.colored('Albus#2627', color='yellow')}... STATUS: ", end='')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

db = sqlite3.connect('Testing/server.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS verified(member_id TEXT, github_uid TEXT)""")
db.commit()

sql.close()
db.close()


BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = discord.Client(intents=intents)
termcolor.cprint('Ready', 'green')

prefix_ = ''



if __name__ == '__main__':
    

    @bot.event
    async def on_ready():
        print('Albus#2627 is online...\n\nLogs:-')
        emd = embed(Colour.blurple(), 'None', "I'm online now...", 'Bot Status')
        await bot.get_channel(1027193457002958959).send(embed=emd)


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
                    # f'Command: **`{cmd}`**\nInfo:- **```{cmd_info}```**'
                    emd = embed(Colour.blurple(), f'$help {cmd[0]}', cmd_info)
                    await channel.send(embed=emd)

                except IndexError as IE: print("error in help commannd", IE)

            else:
                with open('Database/commands.txt', 'r') as cmd_file:
                    cmds = cmd_file.read()

                title = f"Active Prefix Symbol:- ``{prefix}``"
                emd = embed(Colour.blurple(), '$help', cmds, title)
                await channel.send(embed=emd)

        # info command
        elif message == f'{prefix}info':
            emd = embed(Colour.blurple(), message, bot_info, footer=bot_info_foot)

            await channel.send(embed=emd)

        # ping command
        elif message == f'{prefix}ping':

            ping = str(int(round(bot.latency, 2) * 100))
            emd = embed(Colour.blurple(), message, f'{ping}ms')

            await channel.send(embed=emd)

        # prefix change command
        elif message.startswith(f'{prefix}prefix'):
            new_prefix = message.split(' ')[-1]
            msg_link = txt.jump_url

            try: 
                change_status = dotenv.set_key('Database/SECRETS.env', 'PREFIX', new_prefix)
                if change_status[0] is True:
                    msg = f"prefix updated to '{new_prefix}'"
                    emd = embed(Colour.blurple(), message, msg)

                    await channel.send(embed=emd)

                else:
                    msg = f"Unable to update prefix to '{new_prefix}'"
                    emd = embed(Colour.red(), message, msg, 'Facing Error')

                    await channel.send(embed=emd)

            except Exception as E:
                msg = f"error in '{prefix}prefix' command"
                foot_msg = f'message jump link:- {msg_link}'
                emd = embed(Colour.red(), message, msg, 'Facing Error', foot_msg)
                issue_channel = bot.get_channel(1027193550007435334)

                await issue_channel.send(embed=emd)

        # verify command
        elif message.startswith(f'{prefix}verify'):
            db = sqlite3.connect("Testing/server.db")
            sql = db.cursor()

            github_verification_id = str(message.split(' ')[-1])
            msg_link = txt.jump_url

            sql.execute("SELECT member_id FROM verified")
            verified_members = filter_data(sql.fetchall())
            print(verified_members)

            sql.execute("SELECT github_uid FROM verified")
            verified_github_ids = filter_data(sql.fetchall())
            print(verified_github_ids)

            if author in verified_members:
                await channel.send("```You're already verified```")
                
            elif github_verification_id in verified_github_ids:
                await channel.send("```This githun userID is already verified```")

            else:
                sql.execute("""INSERT INTO verified(member_id, github_uid) 
                            VALUES(?, ?)""", (author, github_verification_id))
                db.commit()

                sql.close()
                db.close()

        # bot reboot command (only for dev use)
        elif message == '$reboot$':

            if author == OWNER_ID:
                botID = str(bot.user)
                msg = f'{botID} Will be updated within 5 to 7 seconds...'
                foot_msg = 'Note:- use this command only for development purposes.'
                emd = embed(Colour.orange(), message, msg, 'Admin Command', footer=foot_msg)

                await channel.send(embed=emd)
                os.system(r'py .\bot.py')

            else:
                msg = f"User {author} don't have the permissions to reboot the bot"
                foot_msg = 'Note:- use this command only for development purposes.'
                emd = embed(Colour.red(), message, msg, 'Forbidden', footer=foot_msg)

                await channel.send(embed=emd)

        # bot shutdown commandb
        elif message == '$shutdown$':
            if author == OWNER_ID: quit(); exit()
            else: 
                msg = f"User {author} don't have the permissions to shutdown the bot"
                emd = embed(Colour.red(), message, msg, 'Forbidden')
                await channel.send(embed=emd)


    bot.run(BOT_TOKEN)