# pull oficial base image
FROM python:3.11.4


# set work directory
WORKDIR /usr/src/app

RUN apt update
RUN apt install -y libpq-dev
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .
