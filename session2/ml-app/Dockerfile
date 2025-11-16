# Use official Python runtime as base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy all application code to the container
COPY . .

# Create models directory for storing trained models
RUN mkdir -p models

# Expose port (if you have a web API later)
EXPOSE 5000

# Default command: run training
CMD ["python", "src/train.py"]
