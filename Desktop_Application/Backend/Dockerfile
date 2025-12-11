# Desktop_Application/Backend/Dockerfile
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

# Upgrade pip, setuptools, wheel to avoid build/hash issues
RUN python -m pip install --upgrade pip setuptools wheel

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project
COPY . .

# Expose port
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
