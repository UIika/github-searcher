FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry==2.1.2

COPY . /app
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
