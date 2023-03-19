# pull official base image
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apk update
RUN apk add curl

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /code
RUN pip install -r requirements.txt

# copy project
COPY . .

ENV FLASK_APP main.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 8005
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 8005

CMD ["flask", "run"]

FROM builder AS dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

CMD ["flask", "run"]