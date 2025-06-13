from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

def check_gmails_with_emailscan(gmails):
    valid_emails = []
    # Configuration headless pour Railway
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        for i in range(0, len(gmails), 10):
            batch = gmails[i:i+10]
            gmails_input = "\n".join(batch)
            driver.get("https://emailscan.in")
            time.sleep(2)
            textarea = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div[2]/div/div[1]/div/textarea')
            textarea.clear()
            textarea.send_keys(gmails_input)
            check_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div[2]/div/div[2]/div[2]/div[2]/button[2]')
            check_button.click()
            time.sleep(5)
            # Récupération directe du texte (plus fiable que pyperclip sur Railway)
            valid_emails_elements = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-col.gap-2 > div > div > div > div > div > div > span")
            batch_valid = [el.text for el in valid_emails_elements if el.text]
            valid_emails.extend(batch_valid)
            time.sleep(2)
    finally:
        driver.quit()
    return valid_emails

@app.route('/check_gmails', methods=['POST'])
def check_gmails():
    data = request.get_json()
    gmails = data.get("emails", [])
    valid_gmails = check_gmails_with_emailscan(gmails)
    return jsonify({"valid_emails": valid_gmails})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)