FROM python:3.11-alpine
LABEL authors="antonchuvashov"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install wheel setuptools pip --upgrade
RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev libpq-dev
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 3000
COPY .. .
CMD ["python", "main.py"]