# Stage 1: "builder"
FROM python:3.12 AS builder

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: "runtime"

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
# above dont write /app use only .
COPY data/ ./data/

RUN mkdir -p /app/output \
&& chown app /app/output
 # write without .

USER app

CMD ["python", "app/etl.py"]