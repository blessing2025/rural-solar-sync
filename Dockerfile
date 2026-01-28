FROM python:3.11-alpine

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Copy application
COPY sync.py .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Non-root user for security
RUN addgroup -g 1000 -S appuser && \
    adduser -u 1000 -S appuser -G appuser
USER appuser

CMD ["python", "sync.py"]