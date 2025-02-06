FROM python:3.12-slim

COPY main.py pyproject.toml /
COPY /bearification /bearification
RUN pip install .

ENTRYPOINT ["python3", "-u", "main.py"]
