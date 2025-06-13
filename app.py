from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def check_gmails_with_emailscan(gmails):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    valid_emails = []
    try:
        for i in range(0, len(gmails), 10):
            batch = gmails[i:i+10]
            gmails_input = "\n".join(batch)
            driver.get("https://emailscan.in")
            time.sleep(2)
            # 1. Remplir la textarea
            textarea = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div[2]/div/div[1]/div/textarea')
            textarea.clear()
            textarea.send_keys(gmails_input)
            # 2. Cliquer sur "Check"
            check_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div[2]/div/div[2]/div[2]/div[2]/button[2]')
            check_button.click()
            time.sleep(5)
            # 3. Cliquer sur "Copy Good results"
            copy_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div[2]/div/div[2]/div[3]/div/div[1]/div/div/button[1]')
            copy_button.click()
            time.sleep(1)
            # 4. Récupérer les gmails valides depuis le presse-papier
            import pyperclip
            batch_valid = pyperclip.paste().strip().split('\n')
            valid_emails.extend([e for e in batch_valid if e])
            time.sleep(2)
    except Exception as e:
        print("Erreur Selenium:", e)
    finally:
        driver.quit()
    return valid_emails
