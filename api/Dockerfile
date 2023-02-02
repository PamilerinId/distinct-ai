FROM python:3.9.6

WORKDIR /api

ADD . /api

RUN apt install libpq-dev
RUN pip install -r requirements.txt;

CMD ["python", "app.py"]