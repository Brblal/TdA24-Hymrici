# syntax=docker/dockerfile:1
FROM python

WORKDIR /app


RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
COPY . .
CMD ["./start.sh"]
