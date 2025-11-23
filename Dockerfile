FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt ./requirements.txt
COPY ./app /app
COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /app

EXPOSE 8000

RUN pip install -r /requirements.txt && \
    apk add --no-cache su-exec && \
    adduser --disabled-password --no-create-home duser && \
    chmod -R +x /entrypoint.sh

ENV PATH="/scripts:/venv/bin:$PATH"

CMD ["/entrypoint.sh"]