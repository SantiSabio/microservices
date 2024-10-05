FROM python:3.9

WORKDIR /

COPY ../docs/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["python", "run.py"]
