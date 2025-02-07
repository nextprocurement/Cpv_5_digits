# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY app/requirements.txt /app/requirements.txt

COPY app/ app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the Flask app
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app/main.py"]
