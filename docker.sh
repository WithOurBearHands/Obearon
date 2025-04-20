#!/bin/bash

source venv/bin/activate

alembic upgrade head || exit 1
python3 -u main.py
