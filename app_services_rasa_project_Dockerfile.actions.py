# rasa/Dockerfile.actions
FROM python:3.9-slim

WORKDIR /app
COPY actions/requirements-actions.txt .
RUN pip install --no-cache-dir -r requirements-actions.txt

COPY actions /app/actions
USER 1001

CMD ["python", "-m", "rasa_sdk", "--actions", "actions"]