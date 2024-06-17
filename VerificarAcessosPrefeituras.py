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
# block "Select a certificate" dialog
chrome_options.add_argument("--disable-client-certificate-type")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-popup-blocking")


driver = webdriver.Chrome(
    service=Service(executable_path=CHROME_DRIVER), options=chrome_options
)

wait = WebDriverWait(driver, 10)

status_login = ""


"""
Funções para resolver o captcha de Guarulhos.
"""


def resolve_captcha_brasilia():
    api_key = os.getenv("APIKEY_2CAPTCHA", "8b05577f4418224a86a76ff3bd2b6474")
    solver = TwoCaptcha(api_key)

    for _ in range(3):
        try:
            result = solver.recaptcha(
                sitekey="6Ldl5RsTAAAAAIMRUmK5FUITVtcd6RMjo0Ysuqlj",
                url="https://www2.agencianet.fazenda.df.gov.br/DarAvulso/",
            )
        except Exception as e:
            print(f"A tentativa falhou: {e}\n Repetição de tentativas...")
        else:
            return result

    sys.exit("Falha ao resolver o captcha após 3 tentativass.")
    pass


def resolve_captcha_rio_de_janeiro(
    driver,
    login,
    senha,
    entrar_ID="ctl00_cphCabMenu_btEntrar",
    max_tentativas=5,
    api_key="8b05577f4418224a86a76ff3bd2b6474",
    captcha_xpath="/html/body/form/div[3]/div[1]/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/img",
    error_message_xpath="/html/body/form/div[3]/div[1]/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/span",
    login_ID="ctl00_cphCabMenu_tbCpfCnpj",
    senha_ID="ctl00_cphCabMenu_tbSenha",
):
    for tentativa in range(1, max_tentativas + 4):
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
            driver.find_element(
                By.XPATH,
                "/html/body/form/div[3]/div[1]/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/div/input",
            ).send_keys(code)

            time.sleep(1)

            wait.until(
                EC.element_to_be_clickable((By.ID, "ctl00_cphCabMenu_btEntrar"))
            ).click()
            time.sleep(1)

            try:
                error_message_element = driver.find_element(
                    By.XPATH, error_message_xpath
                )
                erro_visivel = driver.execute_script(
                    "return window.getComputedStyle(arguments[0]).display !== 'none'",
                    error_message_element,
                )

            except NoSuchElementException:
                print("CAPTCHA resolvido com sucesso. (No error message found)")
                return True

        except Exception as e:
            print(f"Erro ao resolver o CAPTCHA: {e}")
            if tentativa == max_tentativas:
                print("Máximo de tentativas excedido.")
                return False


def lidar_com_login(driver, login, senha, municipio, df, linha_inicial_controle):
    linha_inicial_controle = int(linha_inicial_controle)

    municipios_login = {
        "São Paulo": lambda: "ACESSO POR CERTIFICADO",
        "Barra Mansa": lambda: login_barra_mansa(
            driver, login, senha, linha_inicial_controle
        ),
        "Jaú": lambda: login_jaú(driver, login, senha, linha_inicial_controle),
        "Ituiutaba": lambda: login_ituiutaba(
            driver, login, senha, linha_inicial_controle
        ),
        "Betim": lambda: login_betim(driver, login, senha, linha_inicial_controle),
        "Jataí": lambda: login_jataí(driver, login, senha, linha_inicial_controle),
        "Balneário Camboriú": lambda: login_balneario_camboriu(
            driver, login, senha, linha_inicial_controle
        ),
        "Jardim": lambda: login_jardim(driver, login, senha, linha_inicial_controle),
        "Janaúba": lambda: login_janauba(driver, login, senha, linha_inicial_controle),
        "Américo Brasiliense": lambda: login_americo_brasiliense(
            driver, login, senha, linha_inicial_controle
        ),
        "Birigui": lambda: login_birigui(driver, login, senha, linha_inicial_controle),
        "Açailândia": lambda: login_acailandia(
            driver, login, senha, linha_inicial_controle
        ),
        "Barretos": lambda: login_barretos(
            driver, login, senha, linha_inicial_controle
        ),
        "Altamira": lambda: login_altamira(
            driver, login, senha, linha_inicial_controle
        ),
        "Barreiras": lambda: login_barreiras(
            driver, login, senha, linha_inicial_controle
        ),
        "Jequié": lambda: login_jequie(driver, login, senha, linha_inicial_controle),
        "Belo Horizonte": lambda: login_belo_horizonte(
            driver, login, senha, linha_inicial_controle
        ),
        "Rio de Janeiro": lambda: login_rio_de_janeiro(
            driver, login, senha, linha_inicial_controle
        ),
        "Guarulhos": lambda: login_guarulhos(
            driver, login, senha, linha_inicial_controle
        ),
        "Curitiba": lambda: "ACESSO POR CERTIFICADO",
        # "Curitiba": lambda: login_curitiba(
        #     driver, login, senha, linha_inicial_controle),
        "Brasília": lambda: login_brasilia(driver, linha_inicial_controle),
        "Jundiaí": lambda: login_jundiaí(driver, login, senha, linha_inicial_controle),
        # continuar outros municipios
    }

    if municipio in municipios_login:
        return municipios_login[municipio]()
    else:
        print(f"Sem login configurado para {municipio}")
        return None


# -------------------------------------------------------------------------------------
# ---------- FUNÇÕES DE LOGIN PARA CADA MUNICÍPIO ------------------------------------
# -------------------------------------------------------------------------------------
def login_barra_mansa(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    wait.until(EC.visibility_of_element_located((By.ID, "vUSUARIO_LOGIN"))).send_keys(
        login
    )
    wait.until(EC.visibility_of_element_located((By.ID, "vUSUARIO_SENHA"))).send_keys(
        senha
    )
    wait.until(EC.element_to_be_clickable((By.ID, "BTN_ENTER3"))).click()
    try:
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="TABLECPF"]/div[2]/div'))
        ).click()
        driver.implicitly_wait(50)
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        time.sleep(3)
    except:
        print("Login de " + atual + ":  " + status_login)
        status_login = "LOGIN INVALIDO"
        df.loc[linha_inicial_controle, "Observação"] = status_login


def login_jaú(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR FORMA DE ACESSO"
    print("Login de " + atual + ": " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_ituiutaba(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    driver.find_element(By.ID, "usuario").send_keys(login)
    driver.find_element(By.ID, "senha").send_keys(senha)
    try:
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="closebuttons1btOk"]/table/tbody/tr/td[2]')
            )
        ).click()
        driver.implicitly_wait(8)
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
    except Exception as e:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login


def login_betim(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR FORMA DE ACESSO"
    print("Login de " + atual + ": " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_jataí(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    driver.find_element(By.ID, "formLogin:log").send_keys(login)
    driver.find_element(By.ID, "formLogin:pwd").send_keys(senha)
    driver.find_element(By.ID, "formLogin:patternLogin").click()
    try:
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="user-actions"]/div/span[2]')
            )
        ).text
        driver.implicitly_wait(8)
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except Exception as e:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


def login_balneario_camboriu(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    driver.find_element(By.ID, "cpf").send_keys(login)
    driver.find_element(
        By.XPATH,
        '//*[@id="frmMenuExterno"]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/input',
    ).send_keys(senha)
    driver.find_element(
        By.XPATH,
        '//*[@id="frmMenuExterno"]/table[2]/tbody/tr/td/table/tbody/tr[4]/td/input[1]',
    ).click()
    try:
        usu = driver.find_element(
            By.XPATH, '//*[@id="agrupador-area"]/div[2]/table/tbody/tr/td[3]/div'
        ).text
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


def login_jardim(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR ENDEREÇO DO SITE"
    print("Login de " + atual + ": " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_janauba(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    driver.find_element(By.ID, "j_idt47:login").send_keys(login)
    driver.find_element(By.ID, "j_idt47:senha").send_keys(senha)
    driver.find_element(By.ID, "j_idt47:j_idt60").click()
    try:
        usu = driver.find_element(By.XPATH, '//*[@id="j_idt14:j_idt15"]/i').click()
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


def login_americo_brasiliense(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "FALTA INFORMAÇÃO"
    print("Login de " + atual + ": " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_birigui(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    print("Login de " + atual + ": " + "VERIFICAR FORMA DE ACESSO")
    status_login = "VERIFICAR FORMA DE ACESSO"
    df.loc[linha_inicial_controle, "Observação"] = status_login


def login_acailandia(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR FORMA DE ACESSO"
    print("Login de " + atual + ":  " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_barretos(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR FORMA DE ACESSO"
    print("Login de " + atual + ":  " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_altamira(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    driver.find_element(By.ID, "login-cnpj-tab").click()
    driver.find_element(By.ID, "usuarioCnpj").click()
    driver.find_element(By.ID, "usuarioCnpj").send_keys(login)
    driver.find_element(By.ID, "senhaCnpj").send_keys(senha)
    driver.find_element(By.ID, "botaoCapcthaCnpj").click()
    try:
        usu = driver.find_element(By.XPATH, '//*[@id="menu-button"]/i').click()
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


def login_barreiras(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    driver.find_element(By.ID, "usuario").send_keys(login)
    driver.find_element(By.ID, "senha").send_keys(senha)
    driver.find_element(
        By.XPATH, "/html/body/div/main/div/div/div/div[1]/form/div[4]/span/button"
    ).click()
    try:
        usu = driver.find_element(
            By.XPATH, '//*[@id="app"]/main/div/div/div/div[1]/form/div[2]/div/div/div'
        ).text
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


def login_jequie(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    driver.find_element(By.ID, "usuario").send_keys(login)
    driver.find_element(By.ID, "senha").send_keys(senha)
    driver.find_element(
        By.XPATH, "/html/body/div/main/div/div/div/div[1]/form/div[4]/span/button"
    ).click()
    try:
        usu = driver.find_element(
            By.XPATH, '//*[@id="app"]/main/div/div/div/div[1]/form/div[2]/div/div/div'
        ).text
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


def login_belo_horizonte(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    driver.find_element(By.XPATH, '//*[@id="form"]/div[2]/a/img').click()
    driver.find_element(By.ID, "username").send_keys(login)
    driver.find_element(By.ID, "password").send_keys(senha)
    driver.find_element(By.XPATH, '//*[@id="fm1"]/div[3]/button').click()
    try:
        usu = driver.find_element(
            By.XPATH, '//*[@id="identificacao"]/table/tbody/tr/td[2]/a'
        ).click()
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


from selenium.common.exceptions import NoSuchElementException


def login_rio_de_janeiro(driver, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]

    resolve_captcha_rio_de_janeiro(driver, login, senha)

    try:
        error_message_element = driver.find_element(By.ID, "ctl00_cphCabMenu_vsErros")
        error_message = error_message_element.text
    except NoSuchElementException:

        status_login = "LOGIN VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        return
    
    if (
        "Senha Inválida." in error_message
        or "CPF/CNPJ inválido" in error_message
        or "CPF/CNPJ não possui senha cadastrada." in error_message
    ):
        status_login = error_message
    elif "O código digitado não confere com o código da imagem." in error_message:
        status_login = "ERRO NO CAPTCHA"
    else:
        status_login = "LOGIN VÁLIDO"
        print("Login de " + atual + ":  " + status_login)

    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_guarulhos(driver, login, senha, linha_inicial_controle):
    # verificar acesso
    atual = df.loc[linha_inicial_controle, "Município"]
    print("Login de " + atual + ": " + "VERIFICAR FORMA DE ACESSO")
    status_login = "VERIFICAR FORMA DE ACESSO"
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


# def login_curitiba(driver, login, senha, linha_inicial_controle):
#     atual = df.loc[linha_inicial_controle, "Município"]
#     status_login = "ACESSO POR CERTIFICADO"
#     # Também contém captcha
#     print("Login de " + atual + ": " + status_login)
#     df.loc[linha_inicial_controle, "Observação"] = status_login
#     linha_inicial_controle = linha_inicial_controle + 1


def login_brasilia(driver, linha_inicial_controle):
    """Código para testes // Pulando para não lidar com o captcha atoa"""
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "Pulando"
    print("Login de " + atual + ": " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1

    # atual = df.loc[linha_inicial_controle, "Município"]
    # login = df.loc[linha_inicial_controle, "CNPJ"]
    # error_message_XPATH = "/html/body/div[1]/fieldset/div/span"
    # recaptcha_response = "g-recaptcha-response"
    # login_id = "TxtNumDocumento"
    # entrar_id = "BtnSalvar"
    # sair_id = "Logout"

    # driver.get("https://www2.agencianet.fazenda.df.gov.br/DarAvulso/")
    # wait.until(EC.presence_of_element_located((By.ID, login_id))).send_keys(login)
    # wait.until(EC.presence_of_element_located((By.ID, "id="recaptcha-anchor-label""))).click()
    # result = resolve_captcha_brasilia()
    # driver.execute_script(
    #     f"document.getElementById('{recaptcha_response}').style.display = 'block';"
    # )
    # wait.until(EC.presence_of_element_located((By.ID, recaptcha_response))).send_keys(
    #     result["code"]
    # )
    # wait.until(EC.presence_of_element_located((By.ID, entrar_id))).click()
    # time.sleep(2)
    # if EC.presence_of_element_located((By.ID, sair_id)):
    #     status_login = "LOGIN VALIDO"
    #     print("Login de " + atual + ":  " + status_login)
    #     df.loc[linha_inicial_controle, "Observação"] = status_login

    # elif EC.presence_of_element_located((By.XPATH, error_message_XPATH)):
    #     status_login = "LOGIN INVALIDO"
    #     print("Login de " + atual + ":  " + status_login)
    #     df.loc[linha_inicial_controle, "Observação"] = status_login
    # else:
    #     status_login = "ERRO AO ACESSAR"
    #     print("Login de " + atual + ":  " + status_login)
    #     df.loc[linha_inicial_controle, "Observação"] = status_login


def login_jundiaí(driver, login, senha, linha_inicial_controle):
    print("Login Jundiaí")
    atual = df.loc[linha_inicial_controle, "Município"]
    wait.until(EC.visibility_of_element_located((By.ID, "usuario"))).send_keys(login)
    wait.until(EC.visibility_of_element_located((By.ID, "senha"))).send_keys(senha)
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[1]/form/div/div/div/div[4]/div/button")
        )
    ).click()

    try:
        wait.until(EC.visibility_of_element_located((By.ID, "empresas")))
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)

        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


# def ...

""" 
                ---------------------------------------------------------
                ---------------------------------------------------------

                    Insira aqui as funções de login para cada novo município

                ---------------------------------------------------------
                ---------------------------------------------------------

"""


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

tentativas_login = set()  # Armazena as tentativas de login

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
 while linha_inicial_controle < 25:
     linha_inicial_controle = processar_linha_controle(driver, df, linha_inicial_controle, tentativas_login)
"""
