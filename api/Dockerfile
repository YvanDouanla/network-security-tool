FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY api/requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --no-create-home appuser

COPY network_check.py /app/network_check.py
COPY api/main.py /app/api/main.py

USER 10001:10001

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
