# DSA Discord Bot

This bot shall be used for the German P&P role-playing game "The Dark Eye" (German: "Das Schwarze Auge (DSA)") when being played on a Discord-Server.

Included functionality:
- `.roll` : simple skill-check rolling (with "3d20" / "1W6")
- `.check` : storing charakter-sheets with attributes & check for skills, auto-filling attributes 
- WIP:
	- managing charakter-sheet entries
	- Playing music playlist created before-hand for DM only (Sources: Youtube, Google Play Music)


## Setup

Requirements:
- [Git](https://git-scm.com/)
- [Python3](https://www.python.org/downloads/)

Recommended Software:
- [VSCode](https://code.visualstudio.com/) as IDE
- [TortoiseGit](https://tortoisegit.org/) for easier usage of Git (on Windows)

Getting Started:
Use [venv](https://medium.com/python-pandemonium/better-python-dependency-and-package-management-b5d8ea29dff1) to install dependencies, provide config details and start bot.

Initial Setup on Windows:
```bash
mkdir .venv
py -m  venv .venv		# create venv
.\.venv\Scripts\activate		# enter venv
pip3 install -r .\requirements.txt		# install dependencies
copy config.yaml.example config.yaml		# make copy of config-file
# add details in config.yaml
python .\bot\bot.py		# start bot
```
Initial Setup on Linux:
```bash
mkdir .venv
python3 -m venv .venv
source .venv/bin/activate
pip3 install install -r ./requirements.txt
cp config.yaml.example config.yaml
# add details in config.yaml
python3 bot/bot.py		# start bot
```

## Developer Information & Tips

### Discord-Bot

The discord-bot is built on _discord.py_ (see [GitHub](https://github.com/Rapptz/discord.py)).
A is much material on working with this library, including a [simple Youtube-playlist Tutorial](https://www.youtube.com/watch?v=nW8c7vT6Hl4&list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ) or directly the [official documentation](https://discordpy.readthedocs.io/en/latest/index.html).

### Python dependencies

Freezing new dependencies into _requirements.txt_ is done by `$ pip freeze > requirements.txt`.