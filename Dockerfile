FROM python:3.9-alpine3.17
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    mysql-client \
    mariadb-connector-c-dev \
    build-base \
    python3-dev \
    linux-headers \
    libxml2-dev \
    libxslt-dev \
    jpeg-dev \
    zlib-dev \
    tzdata \
    vim \
    && pip install --upgrade pip

WORKDIR /qna

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

