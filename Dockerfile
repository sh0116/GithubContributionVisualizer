# Base Image
FROM python:3.8-slim-buster

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application
COPY . /app
WORKDIR /app

# Run the application
CMD ["python", "main.py"]
