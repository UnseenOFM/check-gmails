FROM selenium/standalone-chrome:latest

USER root

WORKDIR /app
COPY . /app

# Donne les droits d'exécution et crée un lien symbolique pour chromedriver
RUN chmod +x /opt/selenium/chromedriver-137.0.7151.68 && \
    ln -sf /opt/selenium/chromedriver-137.0.7151.68 /usr/bin/chromedriver

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
