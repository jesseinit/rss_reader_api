# Build
FROM python:3.9.5-slim as builder
RUN apt-get update \
  && apt-get install gcc python-dev libpq-dev -y \
  && apt-get clean

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

COPY . /app

# App
FROM python:3.9.5-slim as app

COPY --from=builder /opt/venv /opt/venv

COPY --from=builder /app /app

WORKDIR /app

RUN apt-get update && apt-get install libpq-dev libmagic1 -y

ENV PATH=/opt/venv/bin:/usr/pgsql-9.1/bin/:/root/.local/bin:$PATH

COPY api.sh api.sh

RUN chmod +x api.sh

ENTRYPOINT [ "bash" ]

CMD ["api.sh"]
