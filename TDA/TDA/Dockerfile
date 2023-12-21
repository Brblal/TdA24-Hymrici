# syntax=docker/dockerfile:1
FROM python

WORKDIR /app


RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
COPY . .
EXPOSE 80
RUN chmod +x start.sh
CMD ["TDA/start.sh"]
