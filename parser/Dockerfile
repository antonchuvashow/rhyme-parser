FROM python:3.11
LABEL authors="antonchuvashov"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "api.py"]