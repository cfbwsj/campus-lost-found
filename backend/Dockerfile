# Use Python 3.9 official image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies from official PyPI
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create upload directories
RUN mkdir -p uploads/images uploads/ocr uploads/classify

# Expose port
EXPOSE 8000

# Start command (support PORT env variable for Render)
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"