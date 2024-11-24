# Use Python 3.12.7 slim-bullseye as base image
FROM python:3.12.7-slim-bullseye

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Set working directory inside container
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Set the default command to run the application
CMD ["python", "app.py"]
