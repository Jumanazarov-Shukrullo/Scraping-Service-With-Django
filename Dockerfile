# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt update && apt install -y libpq-dev gcc

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory
COPY . .

# Collect static files (optional, if your app uses static files)
RUN python manage.py collectstatic --no-input

# Set the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "scraping_service_django.wsgi:application"]
