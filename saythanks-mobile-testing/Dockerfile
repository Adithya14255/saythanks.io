FROM python:3.6-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy test files
COPY tests/ tests/
COPY config/ config/
COPY utils/ utils/

# Create reports directory
RUN mkdir -p reports

# Create test runner script
COPY test_runner.py .

# Set environment variables
ENV PYTHONPATH=/app

# Default command
CMD ["python", "test_runner.py"]