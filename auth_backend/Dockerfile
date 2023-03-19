# pull official base image
FROM python:3.10.7-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

ENV FLASK_APP main.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 8005
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 8005

CMD ["flask", "run"]