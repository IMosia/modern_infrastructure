FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir psutil
CMD ["python", "process_analyser.py"]
