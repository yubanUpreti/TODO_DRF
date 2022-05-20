FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add --virtual .build-deps \
    ca-certificates gcc linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev libc-dev \
    curl postgresql-dev

RUN pip install --upgrade pip

RUN adduser -D todo_app

ENV HOME /home/todo_app

ENV APP_DIR ${HOME}/project

ENV PATH "$PATH:/home/todo_app/.local/bin"

WORKDIR ${APP_DIR}

ADD ../requirements.txt ${APP_DIR}/

ADD .env ${APP_DIR}/

RUN pip install -r ${APP_DIR}/requirements.txt

COPY .. ${APP_DIR}

USER todo_app

EXPOSE 8000

ENTRYPOINT sh -c "python manage.py wait_for_db && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
