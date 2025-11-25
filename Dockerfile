FROM python:3.11-slim

# Install dependencies untuk Chrome dan Selenium
RUN apt-get update && apt-get install -y wget gnupg unzip curl && apt-get install -y make

# Tambahkan kunci repository Chrome
RUN wget -q -O /usr/share/keyrings/google-linux-signing-keyring.gpg https://dl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Set working directory
WORKDIR /app

COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir selenium pytest pytest-html pytest-metadata python-dotenv webdriver-manager

# Jalankan pytest by default
CMD ["pytest", "--disable-warnings", "-q"]
