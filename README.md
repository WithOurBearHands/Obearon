# Obearon

## Requirements

- [Python 3.13](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/#installation)
- Mail account that supports IMAP

## Setup

Create a venv and install packages
```bash
uv sync
```

Activate the virtual environment
```bash
.venv\Scripts\activate
```

You can also run anything outside of the venv through (i.E.)
```bash
uv run python main.py
```


## Linting

These tools will format and analyze your code quality automatically:
```bash
black .
isort .
pylint main.py obearon
```
