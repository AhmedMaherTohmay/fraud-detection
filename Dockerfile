# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install Git and Git LFS
RUN apt-get update && \
    apt-get install -y git git-lfs && \
    git lfs install

# Set current working directory
WORKDIR /usr/FraudDetection

# Copy only the requirements.txt initially
COPY requirements.txt /usr/FraudDetection/

# Install the required libraries 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /usr/FraudDetection/

# Ensure Git LFS fetches the actual large files
RUN git lfs fetch && git lfs checkout

# Expose the port within Docker
EXPOSE 5000

# Use Gunicorn to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]