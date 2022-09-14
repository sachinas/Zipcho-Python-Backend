FROM python:3.8.5

ENV PYTHONUNBYFFERED 1

WORKDIR /code

COPY requirements.txt /code/

RUN pip3 install -r requirements.txt

COPY . /code

EXPOSE 8000
