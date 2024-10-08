FROM selenium/standalone-firefox
FROM python:3.12-slim

RUN apt-get update && apt-get install firefox-esr -y

COPY main.py pyproject.toml .env /
COPY /bearification /bearification
RUN pip install .

ENTRYPOINT ["python3", "-u", "main.py"]
