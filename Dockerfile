FROM zenika/alpine-chrome:latest

USER root
RUN apk add --no-cache python3 py3-pip curl unzip

ENV CHROMEDRIVER_VERSION=137.0.7151.70

# 🧠 Ajusté : on liste d’abord le contenu puis on le place manuellement
RUN curl -Lo /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /tmp/chromedriver && \
    find /tmp/chromedriver -name chromedriver -exec mv {} /usr/local/bin/chromedriver \; && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver /tmp/chromedriver.zip

WORKDIR /app
COPY . /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "app.py"]
