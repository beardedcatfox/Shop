FROM python:3.8

COPY ./store/requirements.txt /

RUN pip install -r requirements.txt

WORKDIR /app

COPY ./store/ /app

COPY ./docker/store/runserver.sh /

RUN chmod +x /runserver.sh

EXPOSE 8001

CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8001']
