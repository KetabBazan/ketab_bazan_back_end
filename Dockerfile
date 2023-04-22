FROM python:3.9-alpine3.16

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev libpq-dev python3-dev
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install django
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]