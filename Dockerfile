FROM python:3.14

COPY . /app
WORKDIR /app
RUN ./scripts/init.sh
CMD ["python3", "main.py"]
