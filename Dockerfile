FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY . .
RUN python -m pip install --no-cache-dir ".[api]" && \
    useradd --no-create-home --uid 10001 appuser

USER 10001:10001
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4).close()" || exit 1

CMD ["python", "cli.py", "serve", "--host", "0.0.0.0", "--port", "8000"]
