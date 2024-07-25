# Dockerfile
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /picture_uploader

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy requirements file
COPY requirements.txt /picture_uploader/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /picure_uploader
COPY . /picture_uploader/

# Make port 800 available to the world outside this container
EXPOSE 800

# Run picture_uploader when the container launches
CMD ["python", "picture_uploader.py"]