from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import os

app = Flask(__name__)

def check_gmails_with_emailscan(gmails):
    print("DEBUG: Gmails reçus:", gmails, flush=True)

    chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    valid_emails = []
    try:
        driver = webdriver.Chrome(options=chrome_options)

        for i in range(0, len(gmails), 10):
            batch = gmails[i:i+10]
            print(f"DEBUG: Batch {i//10+1} envoyé à emailscan.in:", batch, flush=True)
            gmails_input = "\n".join(batch)
            driver.get("https://emailscan.in")
            time.sleep(2)

            try:
                textarea = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div[2]/div/div[1]/div/textarea')
                textarea.clear()
                textarea.send_keys(gmails_input)
                print("DEBUG: Textarea remplie.", flush=True)
            except Exception as e:
                print("ERREUR: Impossible de remplir la textarea:", e, flush=True)
                continue

            try:
                check_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/main/div/div[2]/div/div[2]/div[2]/div[2]/button[2]'))
                )
                driver.execute_script("arguments[0].click();", check_button)
                print("DEBUG: Bouton 'Check' cliqué (via JS).", flush=True)
            except Exception as e:
                print("ERREUR: Impossible de cliquer sur 'Check':", e, flush=True)
                continue

            time.sleep(5)

            # 🧪 DEBUG VISUEL
            try:
                driver.save_screenshot("screenshot.png")
                print("DEBUG: Screenshot saved.", flush=True)
            except Exception as e:
                print("ERREUR: Screenshot failed:", e, flush=True)

            try:
                # ✅ Nouveau XPath plus fiable
                results = driver.find_elements(By.XPATH, '//div[contains(@class, "flex") and contains(@class, "items-center")]/div/span')
                print("DEBUG: Nombre d'éléments trouvés:", len(results), flush=True)
                for el in results:
                    print(" -", el.text, flush=True)

                batch_valid = [el.text for el in results if el.text and '@gmail.com' in el.text]
                print("DEBUG: Emails valides trouvés dans ce batch:", batch_valid, flush=True)
                valid_emails.extend(batch_valid)
            except Exception as e:
                print("ERREUR: Impossible de récupérer les emails valides:", e, flush=True)

            time.sleep(2)
    except Exception as e:
        print("ERREUR Selenium globale:", e, flush=True)
    finally:
        try:
            driver.quit()
        except:
            pass

    print("DEBUG: Emails valides totaux:", valid_emails, flush=True)
    return valid_emails

@app.route('/check_gmails', methods=['POST'])
def check_gmails():
    data = request.get_json()
    print("DEBUG: Données reçues dans la requête:", data, flush=True)

    emails_raw = data.get("emails", [])
    if not isinstance(emails_raw, list):
        gmails = [e.strip() for e in str(emails_raw).replace(",", "\n").splitlines() if e.strip()]
    else:
        gmails = emails_raw

    valid_gmails = check_gmails_with_emailscan(gmails)
    print("DEBUG: Emails valides retournés:", valid_gmails, flush=True)
    return jsonify({"valid_emails": valid_gmails})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
