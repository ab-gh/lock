# lock
a bot to lock discord channels
## Install

Requires Python 3, Discord.py 1.7.1

`python3 -m pip install -U discord.py`

## Setup

In `lock.py`, configure `MOD_ROLE` to be the role which grants permission to use the commands, and `LOCK_CATEGORIES` with a list of the channels you want the bot to lock

## Useage

`+status` displays the channel overrides for the `@everyone` role for each channel in the server

`+lock` sets the channel override for `@everyone` to False for each channel in the configured categories

`+unlock` sets the channel override for `@everyone` to True for each channel in the configured categories

`+ping` sees if the bot is alive
