# Use an official Python runtime as a parent image
FROM python:3.12.2

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container's /app directory
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5863

# Run the Flask application
CMD ["python", "app.py"]