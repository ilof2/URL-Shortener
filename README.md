# URLShortener
> Celem zadania jest stworzenie systemu składającego się z mikroserwisu w
Pythonie, który umożliwia skracanie URL-i przez REST API,
przechowywanie ich w bazie danych oraz przekierowywanie do
oryginalnych adresów. System powinien korzystać z kolejki zadań do
asynchronicznego przetwarzania żądań skracania URL-i, zapewniając
wysoką wydajność i skalowalność.

## Dependencies

* Python = 3.11.*
* pip
* Docker and Docker-compose

## How to start

### Easy way

Just run `docker-compose up` in project folder

### Manual way

All steps describe flow for Linux and MacOS environments. If you use windows, please double check each step if it applicable.

1. Do 'cd' to project's folder

    ```bash
    cd URLShortener
    ```

2. Create python virtual environment

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install python requirements

    ```bash
    pip install -r requirements.txt
    ```

4. Install and start redis server:

    * Macos: https://redis.io/docs/install/install-redis/install-redis-on-mac-os/
    * Linux: https://redis.io/docs/install/install-redis/install-redis-on-linux/

5. Setup all need environment variables

    ```bash
    export FLASK_APP=run
    export FLASK_SETTING=dev # test, dev, prod
    export SQLALCHEMY_DATABASE_URI=sqlite:///url_shortener.db
    export CELERY_BROKER_URL=redis://localhost:redis_port
    export CELERY_RESULT_BACKEND=redis://localhost:redis_port
    ```

6. Upgrade your db

    ```bash
    flask db upgrade
    ```

7. Start Flask application

    ```bash
    flask run --debug -h localhost -p 5000
    ```

8. Create new terminal session, repeat steps 1, 2, 5 and start celery

    ```bash
    celery -A run:celery worker --loglevel INFO
    ```

### Troubleshooting

* Chrome Access denied (403):

    1. go to `chrome://net-internals/#sockets`

    2. click [Flush socket pools]

## How to test

* Start unit tests (not ready):

    ```bash
    python -m pytest .
    ```

* Or just use swagger in root endpoint **(ex. localhost:8000/)**
