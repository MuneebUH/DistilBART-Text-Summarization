# Use Python 3.12 slim-buster as base image
FROM python:3.12-slim-buster

# Update the package list and install required system dependencies
RUN apt update -y && apt install -y --no-install-recommends \
    git \
    awscli

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Upgrade accelerate and transformers (if needed)
RUN pip install --no-cache-dir --upgrade accelerate transformers

# Set the default command to run the application
CMD ["python3", "app.py"]
