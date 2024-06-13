import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_DRIVER = "chromedriver.exe"
BASE_PATH = os.path.join("C:", "Users", "anderson.pereira", "AcessoPrefeituras")
CAPTCHA_IMAGE_PATH = os.path.join(BASE_PATH, "captcha.png")
SYSTEM_IMAGE_PATH = os.path.join(BASE_PATH, "sist.png")



LOGIN = "104321"
SENHA = "NOVACASABAHIA"
SITE_URL = "https://portal.gissonline.com.br/login/index.html"



chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=Service(CHROME_DRIVER), options=chrome_options)
wait = WebDriverWait(driver, 10)

"""
Funções para resolver o captcha de Guarulhos.
"""


def clica_no_numero_guarulhos(driver, number):
    """Cliques na imagem do captcha correspondente ao número fornecido."""
    for counter in range(1, 10):
        element = driver.find_element(By.XPATH, f'//*[@id="vNumero"]/img[{counter}]')
        if str(number) in element.get_attribute("src"):
            element.click()
            return


def resolve_captcha_guarulhos(driver, wait):
    """Tentativas de resolver o captcha de Guarulhos."""
    for attempt in range(3):
        try:
            driver.get(SITE_URL)
            wait.until(EC.presence_of_element_located((By.ID, "frmLogin")))

            driver.find_element(By.ID, "TxtIdent").send_keys(LOGIN)
            driver.find_element(By.ID, "TxtSenha").send_keys(SENHA)
            driver.find_element(By.XPATH, "/html/body").click()

            driver.switch_to.frame("frmDiv")
            image = wait.until(EC.presence_of_element_located((By.NAME, "numSeq2")))
            image.screenshot(CAPTCHA_IMAGE_PATH)

            numbers = [
                int(img.get_attribute("value"))
                for img in driver.find_elements(By.XPATH, "//td/img")
            ]

            driver.switch_to.default_content()
            for number in numbers:
                clica_no_numero_guarulhos(driver, number)

            wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="frmLogin"]/a'))
            ).click()
            print("Captcha resolvido com sucesso!")
            return True 
        
        except Exception as e:
            print(f"Erro ao resolver captcha (tentativa {attempt+1}): {e}")
        return False


resolve_captcha_guarulhos(driver, wait)
"""
Fim das funções para resolver o captcha de Guarulhos.
"""
