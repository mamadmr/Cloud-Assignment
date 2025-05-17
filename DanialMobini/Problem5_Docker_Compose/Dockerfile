FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD ["sh", "-c", "celery -A tasks worker --loglevel=info & flask run --host=0.0.0.0 --port=8000"]