FROM python:3.8.1

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

EXPOSE 5000

RUN pip install -r requirements.txt

COPY . /app

CMD [ "uwsgi", "--ini", "app.ini" ]
