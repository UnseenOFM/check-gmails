FROM zenika/alpine-chrome:latest

# Installe Python 3 et pip
RUN apk add --no-cache python3 py3-pip

WORKDIR /app
COPY . /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
