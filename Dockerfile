FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for pg_isready and building wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates gcc libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
