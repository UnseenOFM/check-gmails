FROM zenika/alpine-chrome:latest

USER root

RUN apk add --no-cache python3 py3-pip

WORKDIR /app
COPY . /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
