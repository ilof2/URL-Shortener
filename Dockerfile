FROM python:3.11.4 as builder

# RUN apt-get update \
#    && apt-get install -y libpng-dev libpq-dev git python-dev python3-dev \
#    && apt-get install -y g++ make wget less ca-certificates openssl \
#    && pip install --no-cache-dir --upgrade pip \
#    && pip install --no-cache-dir pipenv

RUN apt-get update \
    && pip install --no-cache-dir --upgrade pip

ENV PYTHONUNBUFFERED 1
ENV LIBRARY_PATH=/lib:/usr/lib
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.11.4

ENV PYTHONUNBUFFERED 1
ENV LIBRARY_PATH=/lib:/usr/lib
ENV APP_HOST=0.0.0.0
ENV APP_PORT=5000
EXPOSE ${APP_PORT}

COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY . /app
COPY /requirements.txt /app


WORKDIR /app
RUN chmod +x entrypoint.sh
ENV FLASK_APP=run.py
ENV FLASK_SETTING=dev
VOLUME ["/app"]
