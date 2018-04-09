from python:3.6.5-alpine3.7

RUN apk update && \
    apk add \
    build-base \
    libpq=10.3-r0 \
    postgresql-dev=10.3-r0

COPY . /flask-app

WORKDIR /flask-app
RUN pip install -r requirements.txt

ENV FLASK_APP=flaskapp.py
ENV DATABASE_URI=postgres://postgres@postgres/postgres

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "--access-logfile", "-", "--error-logfile", "-", "flaskapp:app"]
