FROM zenika/alpine-chrome:latest
USER root

# Install Python, pip, curl, unzip
RUN apk add --no-cache python3 py3-pip curl unzip

# Set matching ChromeDriver version (compatible with zenika/alpine-chrome:latest = Chrome 124)
ENV CHROMEDRIVER_VERSION=124.0.6367.118

# ✅ CORRECTED: download from official storage.googleapis.com
RUN curl -Lo /tmp/chromedriver_linux64.zip https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /usr/local/bin/chromedriver-linux64 /tmp/chromedriver_linux64.zip

# Python app setup
WORKDIR /app
COPY . /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
