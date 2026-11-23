FROM python:3.13-slim

ARG APP_VERSION="v1 (STABLE)"
ENV APP_VERSION=${APP_VERSION}

WORKDIR /app
COPY server.py .
EXPOSE 8080
CMD ["python", "server.py"]
