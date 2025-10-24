FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
 

# Copy source code
COPY . .

# Run FastAPI with uvicorn
# CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
CMD uvicorn app.main:app --host 0.0.0.0 --port  $APP_PORT