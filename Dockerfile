# Use your prepared base image with Chrome + Python deps
FROM crawler-base:py3.12 AS crawler-server

# Set work directory
WORKDIR /app

# Copy your project files
COPY . /app

# Expose Flask port
EXPOSE 9090

# Default command to run your server
CMD ["python", "app.py"]