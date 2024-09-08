# Dockerfile
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /user_manager

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the dependencies file to the working directory
COPY requirements.txt /user_manager/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /user_manager

# Specify the command to run on container start
CMD ["flask", "run", "--host=0.0.0.0"]