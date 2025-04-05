FROM python:3.12-slim

COPY main.py pyproject.toml /
COPY /obearon /obearon
RUN pip install .

ENTRYPOINT ["python3", "-u", "main.py"]
