import time
import warnings
import pandas as pd
import numpy as np
import pyautogui as py
import pyautogui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import sys
import psutil


def is_chrome_running():
    for process in psutil.process_iter():
        if process.name() == "chrome.exe":
            return True
    return False


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
pyautogui.FAILSAFE = False
warnings.filterwarnings("ignore", category=UserWarning)

# Constantes
ARQUIVO_CONTROLE = "controle.txt"
ARQUIVO_EXCEL = "ValidarAcessoPrefeituras.xlsx"
CHROME_DRIVER = "chromedriver.exe"
CAPTCHA_IMAGE_PATH = os.path.join("captcha.png")
SYSTEM_IMAGE_PATH = os.path.join("sist.png")

with open(ARQUIVO_CONTROLE, "r") as arquivo_controle:
    linha_inicial_controle = int(arquivo_controle.read())
    print("Linha arquivo controle: " + str(linha_inicial_controle))

df = pd.read_excel(ARQUIVO_EXCEL)
linha = df.shape[0]
print(linha)
emp = df["CNPJ"][3]

if not os.path.exists(CHROME_DRIVER):
    raise FileNotFoundError(f"chromedriver.exe não encontrado em: {CHROME_DRIVER}")


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("headless")
chrome_options.add_argument("log-level=3")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--ignore-urlfetcher-cert-requests")

chrome_options.add_argument("--disable-client-certificate-type")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-popup-blocking")


driver = webdriver.Chrome(
    service=Service(executable_path=CHROME_DRIVER), options=chrome_options
)

wait = WebDriverWait(driver, 10)

status_login = ""


""" Esse dicionário é uma tentativa de tornar a função de resolver captcha mais genérica para diferentes municípios.
Caso houver municipios com o mesmo captcha, tentar usar a mesma função para resolver o captcha.
"""
municipios_info_resolve_captcha = {
    "Rio de Janeiro": {
        "captcha_xpath": "/html/body/form/div[3]/div[1]/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/img",
        "error_message_XPATH": "/html/body/form/div[3]/div[1]/div[6]/div/div/div[1]/ul/li",
        "login_ID": "ctl00_cphCabMenu_tbCpfCnpj",
        "senha_ID": "ctl00_cphCabMenu_tbSenha",
        "entrar_ID": "ctl00_cphCabMenu_btEntrar",
        "code_input_xpath": "/html/body/form/div[3]/div[1]/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/div/input",
    },
    # Adicionar mais municípios conforme necessário
}


def resolve_captcha(
    driver,
    login,
    senha,
    captcha_xpath,
    error_message_XPATH,
    login_ID,
    senha_ID,
    entrar_ID,
    code_input_xpath,
    linha_inicial_controle,
    max_tentativas=3,
    api_key="8b05577f4418224a86a76ff3bd2b6474",
):
    for tentativa in range(0, max_tentativas):
        print(f"Tentativa {tentativa}: Iniciando desafio CAPTCHA...")

        try:
            wait.until(EC.presence_of_element_located((By.ID, login_ID))).send_keys(
                login
            )
            wait.until(EC.presence_of_element_located((By.ID, senha_ID))).send_keys(
                senha
            )

            captcha_element = driver.find_element(By.XPATH, captcha_xpath)
            captcha_img_path = "captcha.jpg"
            captcha_element.screenshot(captcha_img_path)
            print("Imagem CAPTCHA salva.")

            solver = TwoCaptcha(api_key)
            result = solver.normal(captcha_img_path)
            code = result["code"]

            print(f"CAPTCHA resolvido: {code}")
            driver.find_element(By.XPATH, code_input_xpath).send_keys(code)

            time.sleep(1)

            wait.until(EC.element_to_be_clickable((By.ID, entrar_ID))).click()
            time.sleep(1)

            try:
                error_message_element = driver.find_element(
                    By.XPATH, error_message_XPATH
                )
                error_message = error_message_element.text
                print("Erro: " + error_message)

                if (
                    "Senha Inválida." in error_message
                    or "CPF/CNPJ inválido" in error_message
                    or "CPF/CNPJ não possui senha cadastrada." in error_message
                ):
                    status_login = error_message
                    print("Login inválido: " + status_login)
                    df.loc[linha_inicial_controle, "Observação"] = status_login
                    linha_inicial_controle += 1

                elif (
                    "O código digitado não confere com o código da imagem."
                    in error_message
                ):
                    print(
                        "Captcha inválido na tentativa"
                        + str(tentativa)
                        + " de "
                        + str(max_tentativas)
                        + ", tentando novamente..."
                    )
                    continue
                else:
                    status_login = "ERRO DE VALIDAÇÃO"
                    print("Login inválido: " + status_login)
                    df.loc[linha_inicial_controle, "Observação"] = status_login
                    linha_inicial_controle += 1

            except NoSuchElementException:
                status_login = "LOGIN VÁLIDO"
                print("Login válido: " + status_login)
                df.loc[linha_inicial_controle, "Observação"] = status_login
                linha_inicial_controle += 1
                return

        except Exception as e:
            print(f"Erro ao resolver CAPTCHA: {e}")
            status_login = "ERRO DE VALIDAÇÃO"
            print("Login inválido: " + status_login)
            df.loc[linha_inicial_controle, "Observação"] = status_login
            linha_inicial_controle += 1


def lidar_com_login(driver, login, senha, municipio, df, linha_inicial_controle):
    linha_inicial_controle = int(linha_inicial_controle)

    municipios_login = {
        "Rio de Janeiro": lambda: login_rio_de_janeiro(
            driver, login, senha, linha_inicial_controle
        ),
    }

    if municipio in municipios_login:
        return municipios_login[municipio]()
    else:
        print(f"Sem login configurado para {municipio}")
        return None


def login_rio_de_janeiro(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]

    resolve_captcha(
        driver,
        login,
        senha,
        **municipios_info_resolve_captcha[atual],
        linha_inicial_controle=linha_inicial_controle,
    )


def processar_linha_controle(driver, df, linha_inicial_controle, tentativas_login):

    site = df["Link"].iloc[linha_inicial_controle]
    login = str(df["LOGIN|SENHA"].iloc[linha_inicial_controle])

    senha = str(df["SENHA"].iloc[linha_inicial_controle])
    municipio = df["Município"].iloc[linha_inicial_controle]

    # Verifica se o login e senha já foram tentados
    if (login, senha) in tentativas_login:
        print(f"Login e senha já tentados para {site}")
        df.at[linha_inicial_controle, "Observação"] = df.at[
            linha_inicial_controle - 1, "Observação"
        ]
    else:
        try:
            if (
                "Certificado" in str(login)
                or "https://isscuritiba.curitiba.pr.gov.br/iss/default.aspx" in site
            ):
                print("ACESSO POR CERTIFICADO - " + municipio)
                df.at[linha_inicial_controle, "Observação"] = "ACESSO POR CERTIFICADO"
            else:
                # Lidar com login (presume que a função existe)
                driver.get(site)
                print(f"Acessando {site}...")
                driver.implicitly_wait(20)
                lidar_com_login(
                    driver, login, senha, municipio, df, linha_inicial_controle
                )
                # Registrar a tentativa de login
                tentativas_login.add((login, senha))

        except Exception as e:  # Captura a exceção específica
            print(f"Erro ao acessar {site}: ")
            df.at[linha_inicial_controle, "Observação"] = "PÁGINA NÃO ABRIU"

    # Salva o progresso e atualiza o DataFrame após cada iteração
    df.to_excel(ARQUIVO_EXCEL, index=False)
    with open(ARQUIVO_CONTROLE, "w") as f:
        f.write(str(linha_inicial_controle + 1))  # Próxima linha a processar

    return linha_inicial_controle + 1


# --- Loop principal ---

try:
    with open(ARQUIVO_CONTROLE, "r") as f:
        linha_inicial_controle = int(f.read())
except FileNotFoundError:
    linha_inicial_controle = 0

tentativas_login = set()

while linha_inicial_controle < linha:
    wait = WebDriverWait(driver, 10)
    linha_inicial_controle = processar_linha_controle(
        driver, df, linha_inicial_controle, tentativas_login
    )
    if linha_inicial_controle == linha:
        with open(ARQUIVO_CONTROLE, "w") as f:

            f.write(str(0))

    if not is_chrome_running():
        break


# Loop para testes
""" 
 while linha_inicial_controle < 50:
     linha_inicial_controle = processar_linha_controle(driver, df, linha_inicial_controle, tentativas_login)
"""
