FROM python:3.12-slim-bookworm

# Update package list and install necessary tools
RUN apt update -y && \
    apt install -y awscli git && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN pip install --upgrade accelerate
RUN pip uninstall -y transformers accelerate
RUN pip install transformers accelerate

CMD ["python3", "app.py"]
