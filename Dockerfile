# Use a lightweight Python image
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy all your project files to the container's /app directory
COPY . /app

# Expose the port that your server will run on (8080 in this case)
EXPOSE 8080

# Set the command to run your app using Python's built-in HTTP server
CMD ["python", "-m", "http.server", "8080"]
