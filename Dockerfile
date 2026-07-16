FROM python:3.14

ARG SERVICE_PATH="shufersal_stores_collector"
COPY . /app
WORKDIR /app
CMD ["python3", "-m", "src.services.${SERVICE_PATH}"]
