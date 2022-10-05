import os

def cls():
    os.system('cls')


def flash_cmd(command: str, author: str):
    if author == 'Albus#2627': pass
    elif ((author != 'Albus#2627') and (command.startswith('.'))): print(f"Command used: {command}\nBy: {author}\n")