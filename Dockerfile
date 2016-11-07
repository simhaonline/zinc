FROM python:3.5-alpine

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade boto3==1.4.0 Django==1.10 "djangorestframework<3.5" requests==2.10.0 \
        redis==2.10.5 zipa==0.3.0 celery==3.1.23 celery_once==0.1.4 \
        json-merge-patch==0.1 django-modeladmin-reorder==0.2

RUN set -ex \
    && apk add --no-cache \
        openssl

ENV DOCKERIZE_VERSION v0.2.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

VOLUME /app
COPY . /app

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
RUN ./manage.py migrate

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]
