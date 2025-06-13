FROM zenika/alpine-chrome:latest

USER root
RUN apk add --no-cache python3 py3-pip curl tar

ENV CHROMEDRIVER_VERSION=137.0.7151.70

RUN curl -Lo /tmp/chromedriver.tar.gz https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64/chromedriver-linux64.tar.gz && \
    mkdir -p /tmp/chromedriver && \
    tar -xzf /tmp/chromedriver.tar.gz -C /tmp/chromedriver && \
    mv /tmp/chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver /tmp/chromedriver.tar.gz

WORKDIR /app
COPY . /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "app.py"]
