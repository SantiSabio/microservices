FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV DATABASE_URI=mysql://root:password@mysql_container/inventory_db

CMD ["flask", "run", "--host=0.0.0.0"]