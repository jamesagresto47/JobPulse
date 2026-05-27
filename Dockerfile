FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for persistent data
RUN mkdir -p /data

# Set the environment variable so your Python code knows where to look
ENV DB_DIR=/data

# Copy the application code
COPY . .

# Command to run the application
CMD ["python", "-m", "jobpulse.main"]
