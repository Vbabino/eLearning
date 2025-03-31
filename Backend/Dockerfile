FROM python:3.12-slim

WORKDIR /app

COPY Backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY Backend/ ./

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]