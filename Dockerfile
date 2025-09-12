# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y wget unzip gnupg curl \
    libnss3 libx11-6 libx11-xcb1 libxcomposite1 libxcursor1 \
    libxdamage1 libxi6 libxtst6 libcups2 libxrandr2 \
    libatk1.0-0 libatk-bridge2.0-0 libpangocairo-1.0-0 \
    libgtk-3-0 libgbm1 libasound2 fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Install Chromedriver (latest)
RUN CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE") && \
    wget -q https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip -d /usr/local/bin/ && \
    rm chromedriver-linux64.zip

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --force-reinstall --no-deps -r requirements.txt

# Copy project files
COPY . .

# Expose port Flask runs on
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]