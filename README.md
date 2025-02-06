# Bearification

A Discord bot to verify and link Discord accounts to Warframe accounts.

## Requirements
- [Python 3.12](https://www.python.org/downloads/)

## Setup

Make sure you only install after being in a virtual environment.

```commandline
pip install .
```

## Environment variables

Copy [the example env file](.env.example) into a file called `.env` and fill in the values like this:

| Environment variable   | Description                                               |
|------------------------|-----------------------------------------------------------|
| PROTON_USERNAME        | The ProtonMail username (E-Mail)                          |
| PROTON_PASSWORD        | The ProtonMail password                                   |
| CREATE_MESSAGE_LINK    | Link that should be sent to create a message in the forum |
| DISCORD_TOKEN          | The Discord token for the Discord bot                     |

## Running

To run this application simply execute

```commandline
python main.py
```

### Running from Docker

Build the docker image with:
```commandline
docker build -t bearification:latest .
```

If you haven't run the docker image before, make sure the data folder exists:
```commandline
mkdir data
```

Run the docker image with:
```commandline
docker run -d --name bearification -v=data:/data --env-file=.env bearification:latest
```

## Linting

There are several automatic code formatting tools available.

```commandline
black .
isort .
flake8
pylint main.py bearification
```
