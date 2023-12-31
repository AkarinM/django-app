FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /var/django-app

RUN pip install --upgrade pip poetry==1.6.1
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY mysite .
RUN python manage.py migrate

CMD ['gunicorn', 'mysite.wsgi:application', '--bind', '0.0.0.0:8000']

