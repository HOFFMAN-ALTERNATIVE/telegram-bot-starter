FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml ./
COPY bot ./bot
RUN pip install --no-cache-dir . && useradd -r -u 10001 app
USER app
CMD ["python", "-m", "bot"]
