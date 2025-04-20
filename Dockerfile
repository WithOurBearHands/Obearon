FROM python:3.12-slim

COPY main.py pyproject.toml /
COPY /obearon /obearon
RUN pip install .

COPY docker.sh /docker.sh
RUN chmod +x /docker.sh

ENTRYPOINT ["./docker.sh"]
