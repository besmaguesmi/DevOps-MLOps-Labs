# 1. Start with a lean Python base image
# We use 3.10 to match our ci.yml file
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy requirements and install them *first*
# This is a best practice for Docker caching
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
# Manually install Flask (since it wasn't in the original requirements)
RUN pip install flask

# 4. Copy *only* our source code into the container
# This copies train.py, predict.py, model.py, etc. and the __init__.py
COPY src /app/src

# 5. Expose the port our web app runs on (from src/predict.py)
EXPOSE 5000

# This makes it a "runnable container that exposes the app port"
CMD ["python", "src/predict.py"]