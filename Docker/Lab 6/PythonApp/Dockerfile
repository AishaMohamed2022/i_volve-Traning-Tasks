FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
# Hardcoded default environment variables
ENV APP_NAME=iVolveApp3
ENV APP_ENV=dev
EXPOSE 5000

CMD ["python", "app.py"]