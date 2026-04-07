FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/deps -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /deps /usr/local/lib/python3.11/site-packages
COPY --from=builder /deps/bin/* /usr/local/bin/
COPY src/ /app/
RUN groupadd -r pyraclaw && useradd -r -g pyraclaw pyraclaw \
    && chown -R pyraclaw:pyraclaw /app \
    && apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
USER pyraclaw
ENV PYTHONPATH=/app PORT=8010 PYTHONUNBUFFERED=1
EXPOSE 8010
HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8010/health || exit 1
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010", "--workers", "2"]
