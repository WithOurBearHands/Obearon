#!/bin/bash

source venv/Scripts/activate

alembic upgrade head || exit 1
python3 -u main.py
