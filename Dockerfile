# syntax=docker/dockerfile:1

FROM python:3.10-buster

WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy

COPY . .

EXPOSE 80
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]

