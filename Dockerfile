FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY task_api.py .

EXPOSE 5000

CMD ["python", "task_api.py"]

