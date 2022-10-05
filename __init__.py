import os
import dotenv

def cls():
    os.system('cls')


def flash_cmd(command: str, author: str):
    prefix = dotenv.get_key('Database/SECRETS.env', 'PREFIX')

    if author == 'Albus#2627': pass
    elif ((author != 'Albus#2627') and (command.startswith(prefix))): print(f"Command used: {command}\nBy: {author}\n")