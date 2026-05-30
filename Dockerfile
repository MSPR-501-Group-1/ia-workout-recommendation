# ─────────────────────────────────────────
#  IA WORKOUT RECOMMENDATION SERVICE
# ─────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

RUN chmod +x /app/scripts/start.sh

# Security: run as non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://127.0.0.1:8001/docs', timeout=5)" || exit 1

EXPOSE 8001

CMD ["/app/scripts/start.sh"]
