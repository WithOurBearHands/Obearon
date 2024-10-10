FROM selenium/standalone-firefox
FROM python:3.12-slim

RUN apt-get update && apt-get install firefox-esr -y

ARG TARGETARCH
RUN if [ $TARGETARCH = "aarch64" ]; then \
        RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux-aarch64.tar.gz \
        RUN tar -xzvf geckodriver-v0.33.0-linux-aarch64.tar.gz -C /usr/local/bin \
        RUN chmod +x /usr/local/bin/geckodriver \
        RUN rm -rf geckodriver-v0.35.0-linux-aarch64.tar.gz \
    ; fi

COPY main.py pyproject.toml .env /
COPY /bearification /bearification
RUN pip install .

ENTRYPOINT ["python3", "-u", "main.py"]
