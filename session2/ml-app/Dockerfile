FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p models
VOLUME ["/app/models"]

# Optional: expose port if needed
# EXPOSE 5000

CMD ["python", "src/train.py"]
