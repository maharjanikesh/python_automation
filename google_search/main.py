from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def google_search(query, limit=5):
    """Perform a stealthy Google search and return results."""
    options = Options()

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://www.google.com")
    time.sleep(2)

    search_box = driver.find_element(By.NAME, "q")
    time.sleep(2)
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
        )
    except:
        print("Page took too long to load.")
        driver.quit()
        return

    results = driver.find_elements(By.CSS_SELECTOR, "h3")

    for i, result in enumerate(results[:limit], start=1):
        try:
            title = result.text
            url = result.find_element(By.XPATH, "./ancestor::a").get_attribute("href")
            print(f"{i}. {title}\n   {url}\n")
        except:
            continue

    driver.quit()


if __name__ == "__main__":
    google_search("Python automation")
