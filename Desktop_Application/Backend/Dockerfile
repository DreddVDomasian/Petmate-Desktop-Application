# Desktop_Application/Backend/Dockerfile.prod
FROM python:3.11-slim

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# system packages (needed for mysqlclient & WeasyPrint)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgobject-2.0-0 \
    libcairo2 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy project
COPY . /app

# collect static
ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python manage.py collectstatic --noinput || true

# create a non-root user (optional but good practice)
RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--log-level", "info", "--access-logfile", "-"]
