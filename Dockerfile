FROM zenika/alpine-chrome:latest

USER root
RUN apk add --no-cache python3 py3-pip curl unzip

COPY chromedriver-linux64.zip /tmp/chromedriver.zip

RUN unzip /tmp/chromedriver.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip

# Vérification debug
RUN ls -al /usr/local/bin && which chromedriver || echo "chromedriver NOT found"

WORKDIR /app
COPY . /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "app.py"]
