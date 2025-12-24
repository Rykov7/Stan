FROM python:3.13-slim-trixie

LABEL title="Stan"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ ./requirements/
RUN ["pip", "install", "-r", "requirements/requirements.txt", "--no-cache-dir", "--disable-pip-version-check"]

COPY . .

EXPOSE 8813

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8813", "wsgi:app"]
