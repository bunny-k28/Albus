import dotenv
import random


# dotenv.load_dotenv('./SECRETS.env')

prefix = dotenv.get_key(dotenv_path='../Database/SECRETS.env', key_to_get='PREFIX')
random_prefix = random.choice(['!', '.', '/', '@', '#', '*', '&'])

help = f"""This command works in two way:- 
1. If you just type {prefix}help, it will show you the list of all commands.
2. If you type {prefix}help <command>, if will show you the info of that specified command.

For Ex:- {prefix}help or {prefix}help {prefix}ping"""

info = "This command tells you about the bot. And the active command prefix of the bot."

ping = "This command will show you the latency/ping of the bot host network."

prefix_ = f"""This command helps you to change the active prefix of the bot command. 
You just have to type {prefix}prefix <new_prefix>. The prefix will be updated that moment.

For Ex:- {prefix}prefix {random_prefix}"""


cmd_details = {
    f'{prefix}help': help, 
    f'$info': info, 
    f'{prefix}ping': ping, 
    f'{prefix}prefix': prefix_}