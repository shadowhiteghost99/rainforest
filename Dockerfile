FROM python:3.14

ARG EXECUTOR_TYPE="shufersal/collectors/store"
COPY . /app
WORKDIR /app
RUN ./scripts/init.sh
CMD ["python3", "main.py", "${EXECUTOR_TYPE}/main.py"]
