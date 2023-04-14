FROM python:3.8

COPY ./shop/requirements.txt /

RUN pip install -r requirements.txt

WORKDIR /app

COPY ./shop/ /app

COPY ./docker/shop/runserver.sh /

RUN chmod +x /runserver.sh

EXPOSE 8000

CMD ["/runserver.sh"]
