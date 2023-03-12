FROM python:3.9

COPY ./requirements_test.txt /tmp/requirements_test.txt

RUN set -x \
    && python -m venv /opt/server \
    && /opt/server/bin/python -m pip install -U pip wheel setuptools httpx alembic psycopg2-binary \
    && /opt/server/bin/python -m pip install --no-cache-dir -q -r /tmp/requirements_test.txt \
    && mkdir -p /workspace

WORKDIR /workspace

ENV PATH="/opt/server/bin:${PATH}"

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /workspace

WORKDIR /workspace/server
