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

RUN groupadd --gid 10001 app \
 && useradd --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app

COPY --from=builder /opt/venv /opt/venv
#refers to requirements.txt

COPY app/ .
# above dont write /app use only .
COPY data/ ./data/

RUN mkdir -p /app/output \
&& chown app:app /app/output
 # write without .

USER app

CMD ["python", "report.py"]