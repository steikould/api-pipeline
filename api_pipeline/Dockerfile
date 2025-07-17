# Dockerfile for Cloud Run Jobs
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Your CLI application becomes the entry point
CMD ["python", "-m", "your_package", "--config", "pipeline_config.yaml", "--concurrent", "--status-file", "/tmp/status.json"]