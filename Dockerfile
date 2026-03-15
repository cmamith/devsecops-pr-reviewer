FROM python:3.12-slim

WORKDIR /app

# Copy requirement files and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY main.py agents.py tasks.py ./

# Define the entrypoint for the Docker container
ENTRYPOINT ["python", "/app/main.py"]
