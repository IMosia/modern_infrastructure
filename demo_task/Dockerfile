FROM python:3.8-slim
WORKDIR /app
COPY . /app
COPY .env /app/.env
COPY files_to_check /app/files_to_check
RUN pip install --no-cache-dir psutil python-dotenv
CMD ["python", "process_analyser.py"]
