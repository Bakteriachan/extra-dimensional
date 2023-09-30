FROM python:3.8-slim-buster

WORKDIR /bot/src

COPY src .
COPY require.txt .

RUN pip install -r require.txt

ENV PERSISTANCE_FILENAME="/persistence/persistence_data"
VOLUME /persistence

CMD ["python3", "bot.py"]
