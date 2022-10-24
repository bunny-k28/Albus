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

db = sqlite3.connect('Database/server.db')
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
    async def on_message(ctx):
        global prefix_

        message = str(ctx.content)
        author = str(ctx.author)
        channel = ctx.channel

        OWNER_ID = os.getenv('OWNER_ID')
        prefix = prefix_ = dotenv.get_key('Database/SECRETS.env', 'PREFIX')

        flash_cmd(message, author)

        if ctx.author == bot.user:
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

        # prefix command
        elif message.startswith(f'{prefix}prefix'):
            new_prefix = message.split(' ')[-1]
            msg_link = ctx.jump_url

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

        # dev command
        elif message == f'{prefix}dev':
            db = sqlite3.connect("Database/server.db")
            sql = db.cursor()

            try:
                sql.execute(f"SELECT github_uid FROM verified WHERE member_id='{author}'")
                githubUID = sql.fetchone()[0]
            except Exception as E:
                msg = "You're not verified. 1st verify yourself."
                title = "Verification Status"
                foot_msg = f"To get verified, use `{prefix}verify` cmd. For more use `$help` cmd"
                emd = embed(Colour.blurple(), message, msg, title, foot_msg)

                await channel.send(embed=emd)
                await bot.get_channel(1027193550007435334).send(f'**```Unable to extract user data\nError in dev command\nError: {E}```**')

            details_api_url = f"https://api.github.com/users/{githubUID}"
            repo_count = json.loads(requests.get(details_api_url).content)["public_repos"]
            if repo_count >= 3:
                try:
                    role = get_role(ctx, "Developers 💻")
                    await role[0].add_roles(role[-1])

                    msg = "Now you're a developer."
                    title = "Role Request"
                    emd = embed(Colour.blurple(), message, msg, title)
                    await channel.send(embed=emd)

                except Exception as E:
                    await bot.get_channel(1027193550007435334).send(f"**```Unable to give developer role\nError in dev command\nError: {E}```**")

            else:
                msg = "Can't give you developer role. You don't have much experience."
                title = "Role Request"
                foot_msg = "For developer role your GitHub profile must have >=3 repo"
                emd = embed(Colour.blurple(), message, msg, title, foot_msg)
                await channel.send(embed=emd)

        # verify command
        elif message.startswith(f'{prefix}verify'):
            db = sqlite3.connect("Database/server.db")
            sql = db.cursor()

            github_verification_id = str(message.split(' ')[-1])

            sql.execute("SELECT member_id FROM verified")
            verified_members = filter_data(sql.fetchall())
            # print(verified_members)

            sql.execute("SELECT github_uid FROM verified")
            verified_github_ids = filter_data(sql.fetchall())
            # print(verified_github_ids)

            if author in verified_members:
                msg = "You're already verified"
                title = "Verification Status"
                emd = embed(Colour.blurple(), message, msg, title)
                await channel.send(embed=emd)
                
            elif github_verification_id in verified_github_ids:
                msg = "This GitHub userID is already verified"
                title = "Verification Status"
                emd = embed(Colour.blurple(), message, msg, title)
                await channel.send(embed=emd)

            else:
                verify_status = verify_member(github_verification_id)
                if verify_status[0] is True:
                    try:
                        role = get_role(ctx, "Verified✅")
                        await role[0].add_roles(role[-1])

                        msg = "Now you're verified"
                        title = "Verification Status"
                        foot_msg = "Now you can view all the general channels"
                        emd = embed(Colour.blurple(), message, msg, title)

                        sql.execute("""INSERT INTO verified(member_id, github_uid) 
                                    VALUES(?, ?)""", (author, github_verification_id))
                        db.commit()

                        sql.close()
                        db.close()

                        await channel.send(embed=emd)

                        try:
                            await ctx.author.edit(nick=verify_status[-1])
                        except Exception as E:
                            await bot.get_channel(1027193550007435334).send(f'''**```Unable to change nick-name.\nError in line 168\nError: {E}```**''')

                    except Exception as E:
                        await bot.get_channel(1027193550007435334).send(f'**```Unable to give role.\nError in line 180\nError: {E}```**')

                elif verify_status[0] is False:
                    msg = verify_status[-1]
                    title = "Verification Status"
                    emd = embed(Colour.red(), message, msg, title)
                    await channel.send(embed=emd)

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