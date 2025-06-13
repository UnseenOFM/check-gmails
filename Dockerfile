FROM zenika/alpine-chrome:latest

USER root

# Install Python, pip, unzip, curl
RUN apk add --no-cache python3 py3-pip curl unzip

# Set known Chrome version (zenika image = v124.0.6367.118)
ENV CHROME_VERSION=124.0.6367.118

# Download matching chromedriver
RUN curl -Lo /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /usr/local/bin/chromedriver-linux64 /tmp/chromedriver.zip

# Python setup
WORKDIR /app
COPY . /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
