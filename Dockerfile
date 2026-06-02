FROM python:3.13-slim

# Don't buffer stdout/stderr so logs show up in `docker logs` immediately.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LAST_MENTION_FILE=/data/last_mention.txt

WORKDIR /app

# Install dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY augbot.py .

# Persist mention-streak state outside the image.
RUN mkdir -p /data
VOLUME ["/data"]

# Run as a non-root user.
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app /data
USER appuser

CMD ["python", "augbot.py"]
