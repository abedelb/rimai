# Base image: Ubuntu
FROM ubuntu:22.04

# Prevents interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and required tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv curl && \
    apt-get clean


WORKDIR /app

# Copy app files
COPY ./app /app

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt


# Expose FastAPI port
EXPOSE 8000


# Default command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]