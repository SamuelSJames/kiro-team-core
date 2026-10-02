FROM python:3.12-slim

# Non-root runtime user; /data is the persistent image output mount.
RUN useradd --create-home --uid 10001 app \
    && mkdir -p /data && chown app:app /data

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py .

USER app
ENV ORIMG_OUTPUT_DIR=/data \
    PYTHONUNBUFFERED=1

# stdio MCP server
ENTRYPOINT ["python", "server.py"]
