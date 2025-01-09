# Use an official Python runtime as a parent image
FROM python:3.12.2

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container's /app directory
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Set environment variables for Ollama
ENV PATH="/root/.ollama/bin:$PATH"

# Command to pull and run a model (define here)
RUN ollama run llama3.1:8b

# Expose the application port
EXPOSE 5863

# Run the Flask application
CMD ["python", "app.py"]