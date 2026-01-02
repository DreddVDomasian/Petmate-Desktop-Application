# Use Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for WeasyPrint and mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
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

# Upgrade pip, setuptools, wheel
RUN python -m pip install --upgrade pip setuptools wheel

# Copy and install Python dependencies
COPY Desktop_Application/Backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY Desktop_Application/Backend /app

# Expose port
EXPOSE 8000

# Start command (will be overridden by railway.json)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
