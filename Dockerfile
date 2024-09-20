# Use official Python image from DockerHub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Define the command to start the app (change app:app to application:app)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "application:app"]
