# Use official Python runtime as base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy all application code to container
COPY . .

# Create models directory for storing trained models
RUN mkdir -p models

# Expose port for potential API/web service
EXPOSE 8000

# Set PYTHONPATH to include current directory
ENV PYTHONPATH=/app

# Run Training
CMD ["python", "src/train.py"]
