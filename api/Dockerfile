From python:3.9.6-alpine

WORKDIR /api

ADD . /api

RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	;
RUN pip install -r requirements.txt;
RUN apk del .build-deps;

# CMD ["uwsgi", "app.ini"]
CMD ["python", "app.py"]