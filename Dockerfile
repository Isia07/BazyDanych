FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.py /app/entrypoint.py
RUN chmod +x /app/entrypoint.py

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.py"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]