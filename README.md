# Bearification

A Discord bot to verify and link Discord accounts to Warframe accounts.

## Requirements
- [Python 3.12](https://www.python.org/downloads/)

## Setup
```commandline
pip install .
```

## Environment variables

Copy [the example env file](.env.example) into a file called `.env` and fill in the values like this:

| Environment variable | Description                                                     |
| --- |-----------------------------------------------------------------|
| COOKIE_GID | Cookie called "gid" in the Warframe forums, needed for log in   |
| COOKIE_LOGSIG | Cookie called "logsig", same as above                           |
| COOKIE_IPS4_DEVICE_KEY | Cookie called "ips4_device_key", same as above                  |
| CREATE_MESSAGE_LINK | Link that should be sent to create a message in the forum       |
| DISCORD_TOKEN | The Discord token for the Discord bot                           |

## Running

```commandline
python main.py
```
