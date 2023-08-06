import os
from octosuite import colors
banner = f'''{colors.red}
 ▒█████   ▄████▄  ▄▄▄█████▓ ▒█████    ██████  █    ██  ██▓▄▄▄█████▓▓█████ 
▒██▒  ██▒▒██▀ ▀█  ▓  ██▒ ▓▒▒██▒  ██▒▒██    ▒  ██  ▓██▒▓██▒▓  ██▒ ▓▒▓█   ▀ 
▒██░  ██▒▒▓█    ▄ ▒ ▓██░ ▒░▒██░  ██▒░ ▓██▄   ▓██  ▒██░▒██▒▒ ▓██░ ▒░▒███   
▒██   ██░▒▓▓▄ ▄██▒░ ▓██▓ ░ ▒██   ██░  ▒   ██▒▓▓█  ░██░░██░░ ▓██▓ ░ ▒▓█  ▄ 
░ ████▓▒░▒ ▓███▀ ░  ▒██▒ ░ ░ ████▓▒░▒██████▒▒▒█████▓ ░██░  ▒██▒ ░ ░▒████▒
░ ▒░▒░▒░ ░ ░▒ ▒  ░  ▒ ░░   ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░▓    ▒ ░░   ░░ ▒░ ░
  ░ ▒ ▒░   ░  ▒       ░      ░ ▒ ▒░ ░ ░▒  ░ ░░░▒░ ░ ░  ▒ ░    ░     ░ ░  ░
░ ░ ░ ▒  ░          ░      ░ ░ ░ ▒  ░  ░  ░   ░░░ ░ ░  ▒ {colors.red_bg}v1.6.0-stable{colors.reset}{colors.red}
    ░ ░  ░ ░                   ░ ░        ░     ░      ░              ░  ░
         ░                              {colors.white}— Advanced Github {colors.red}OSINT{colors.white} Framework{colors.reset}



> {colors.white}Current user: {colors.white_bg}{os.getlogin()}{colors.reset}
> {colors.white}Use {colors.white_bg}help{colors.reset}{colors.white} command for usage{colors.reset}
> {colors.white}Commands are {colors.white_bg}case sensitive{colors.reset}
{'-'*30}


'''