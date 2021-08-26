FROM python:3.8.3-slim

COPY requirements.txt /aviasales_bot/requirements.txt

WORKDIR /aviasales_bot

RUN PYTHONPATH=/usr/bin/python pip install -r requirements.txt

COPY . /aviasales_bot

CMD ["python", "./core.py" ]
