FROM python:3.9-slim

# Set the working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "shortener_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]