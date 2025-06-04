# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install the required system dependencies for building Python packages efficiently
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libatlas-base-dev \
    build-essential \
    git-lfs

# Initialize Git LFS
RUN git lfs install

# Copy the requirements.txt into the container
COPY requirements.txt .  

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt  # Fixed typo!

# Copy the rest of the application code into the container
COPY . .

# Ensure LFS files are properly pulled & checked out
RUN git lfs fetch && git lfs checkout

# Expose port 5000 for Flask
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the Flask app
CMD ["python", "app.py"]