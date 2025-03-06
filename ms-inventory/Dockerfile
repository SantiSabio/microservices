FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uwsgi", "--http", "0.0.0.0:5003", "--module", "run:app", "--processes", "4", "--threads", "2"]