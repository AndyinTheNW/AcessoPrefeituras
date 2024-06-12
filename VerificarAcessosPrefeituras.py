import time
import pandas as pd
import pyautogui as py
import pyautogui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

pyautogui.FAILSAFE = False

# Constantes
ARQUIVO_BASE = "C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\"
ARQUIVO_CONTROLE = "controle.txt"
ARQUIVO_EXCEL = "ValidarAcessoPrefeituras.xlsx"
CHROME_DRIVER = "chromedriver.exe"

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

chrome_options.add_argument("headless")
chrome_options.add_argument("log-level=3")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--ignore-urlfetcher-cert-requests")


browser = webdriver.Chrome(
    service=Service(executable_path=CHROME_DRIVER), options=chrome_options
)

wait = WebDriverWait(browser, 10)

status_login = ""


def lidar_com_login(browser, login, senha, municipio, df, linha_inicial_controle):

    linha_inicial_controle = int(linha_inicial_controle)

    municipios_login = {
        "São Paulo": "ACESSO POR CERTIFICADO",
        "Barra Mansa": login_barra_mansa(browser, login, senha, linha_inicial_controle),
        "Jaú": login_jaú(browser, login, senha, linha_inicial_controle),
        "Ituiutaba": login_ituiutaba(browser, login, senha, linha_inicial_controle),
        "Betim": login_betim(browser, login, senha, linha_inicial_controle),
        "Jataí": login_jataí(browser, login, senha, linha_inicial_controle),
        "Balneário Camboriú": login_balneario_camboriu(
            browser, login, senha, linha_inicial_controle
        ),
        "Jardim": login_jardim(browser, login, senha, linha_inicial_controle),
        "Janaúba": login_janauba(browser, login, senha, linha_inicial_controle),
        "Américo Brasiliense": login_americo_brasiliense(
            browser, login, senha, linha_inicial_controle
        ),
        "Birigui": login_birigui(browser, login, senha, linha_inicial_controle),
        "Açailândia": login_acailandia(browser, login, senha, linha_inicial_controle),
        "Barretos": login_barretos(browser, login, senha, linha_inicial_controle),
        "Altamira": login_altamira(browser, login, senha, linha_inicial_controle),
        "Barreiras": login_barreiras(browser, login, senha, linha_inicial_controle),
        "Jequié": login_jequie(browser, login, senha, linha_inicial_controle),
        "Belo Horizonte": login_belo_horizonte(
            browser, login, senha, linha_inicial_controle
        ),
        "Rio de Janeiro": login_rio_de_janeiro(
            browser, login, senha, linha_inicial_controle
        ),
        "Guarulhos": login_guarulhos(browser, login, senha, linha_inicial_controle),
        "Curitiba": login_curitiba(browser, login, senha, linha_inicial_controle),
        "Jundiaí": login_jundiai(browser, login, senha, linha_inicial_controle),
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
def login_barra_mansa(browser, login, senha, linha_inicial_controle):
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
        browser.implicitly_wait(50)
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        time.sleep(3)
    except:
        print("Login de " + atual + ":  " + status_login)
        status_login = "LOGIN INVALIDO"
        df.loc[linha_inicial_controle, "Observação"] = status_login


def login_jaú(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR FORMA DE ACESSO"
    print("Login de " + atual + ":  " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_ituiutaba(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    browser.find_element(By.ID, "usuario").send_keys(login)
    browser.find_element(By.ID, "senha").send_keys(senha)
    try:
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="closebuttons1btOk"]/table/tbody/tr/td[2]')
            )
        ).click()
        browser.implicitly_wait(8)
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
    except Exception as e:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login


def login_betim(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR FORMA DE ACESSO"
    print("Login de " + atual + ":  " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_jataí(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    browser.find_element(By.ID, "formLogin:log").send_keys(login)
    browser.find_element(By.ID, "formLogin:pwd").send_keys(senha)
    browser.find_element(By.ID, "formLogin:patternLogin").click()
    try:
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="user-actions"]/div/span[2]')
            )
        ).text
        browser.implicitly_wait(8)
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except Exception as e:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


def login_balneario_camboriu(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    browser.find_element(By.ID, "cpf").send_keys(login)
    browser.find_element(
        By.XPATH,
        '//*[@id="frmMenuExterno"]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/input',
    ).send_keys(senha)
    browser.find_element(
        By.XPATH,
        '//*[@id="frmMenuExterno"]/table[2]/tbody/tr/td/table/tbody/tr[4]/td/input[1]',
    ).click()
    try:
        usu = browser.find_element(
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


def login_jardim(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR ENDEREÇO DO SITE"
    print("Login de " + atual + ":  " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_janauba(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    browser.find_element(By.ID, "j_idt47:login").send_keys(login)
    browser.find_element(By.ID, "j_idt47:senha").send_keys(senha)
    browser.find_element(By.ID, "j_idt47:j_idt60").click()
    try:
        usu = browser.find_element(By.XPATH, '//*[@id="j_idt14:j_idt15"]/i').click()
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


def login_americo_brasiliense(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "FALTA INFORMAÇÃO"
    print("Login de " + atual + ":  " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_birigui(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    print("Login de " + atual + ":  " + "VERIFICAR FORMA DE ACESSO")
    status_login = "VERIFICAR FORMA DE ACESSO"
    df.loc[linha_inicial_controle, "Observação"] = status_login


def login_acailandia(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR FORMA DE ACESSO"
    print("Login de " + atual + ":  " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_barretos(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR FORMA DE ACESSO"
    print("Login de " + atual + ":  " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_altamira(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    browser.find_element(By.ID, "login-cnpj-tab").click()
    browser.find_element(By.ID, "usuarioCnpj").click()
    browser.find_element(By.ID, "usuarioCnpj").send_keys(login)
    browser.find_element(By.ID, "senhaCnpj").send_keys(senha)
    browser.find_element(By.ID, "botaoCapcthaCnpj").click()
    try:
        usu = browser.find_element(By.XPATH, '//*[@id="menu-button"]/i').click()
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    except:
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


def login_barreiras(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    browser.find_element(By.ID, "usuario").send_keys(login)
    browser.find_element(By.ID, "senha").send_keys(senha)
    browser.find_element(
        By.XPATH, "/html/body/div/main/div/div/div/div[1]/form/div[4]/span/button"
    ).click()
    try:
        usu = browser.find_element(
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


def login_jequie(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    browser.find_element(By.ID, "usuario").send_keys(login)
    browser.find_element(By.ID, "senha").send_keys(senha)
    browser.find_element(
        By.XPATH, "/html/body/div/main/div/div/div/div[1]/form/div[4]/span/button"
    ).click()
    try:
        usu = browser.find_element(
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


def login_belo_horizonte(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    browser.find_element(By.XPATH, '//*[@id="form"]/div[2]/a/img').click()
    browser.find_element(By.ID, "username").send_keys(login)
    browser.find_element(By.ID, "password").send_keys(senha)
    browser.find_element(By.XPATH, '//*[@id="fm1"]/div[3]/button').click()
    try:
        usu = browser.find_element(
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


def login_rio_de_janeiro(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    browser.find_element(By.ID, "ctl00_cphCabMenu_tbCpfCnpj").send_keys(login)
    browser.find_element(By.ID, "ctl00_cphCabMenu_tbSenha").send_keys(senha)
    time.sleep(3)
    # resolver_captcha(browser)
    # print("captcha resolvido")
    time.sleep(3)
    browser.find_element(
        By.XPATH,
        "/html/body/form/div[3]/div[1]/div[6]/div/div/div[2]/div[1]/div[2]/input",
    ).click()
    time.sleep(3)
    # ctl00_cphCabMenu_vsErros
    if browser.find_elements(By.ID, "ctl00_cphCabMenu_vsErros"):
        status_login = "LOGIN INVALIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1
    else:
        status_login = "VÁLIDO"
        print("Login de " + atual + ":  " + status_login)
        df.loc[linha_inicial_controle, "Observação"] = status_login
        linha_inicial_controle = linha_inicial_controle + 1


def login_guarulhos(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR FORMA DE ACESSO"
    # Contém captcha
    print("Login de " + atual + ":  " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_curitiba(browser, login, senha, linha_inicial_controle):
    atual = df.loc[linha_inicial_controle, "Município"]
    status_login = "VERIFICAR FORMA DE ACESSO"
    # Também contém captcha
    print("Login de " + atual + ":  " + status_login)
    df.loc[linha_inicial_controle, "Observação"] = status_login
    linha_inicial_controle = linha_inicial_controle + 1


def login_jundiai(browser, login, senha, linha_inicial_controle):
    print("Login de Jundiaí")

    atual = df.loc[linha_inicial_controle, "Município"]

    wait.until(EC.visibility_of_element_located((By.ID, "usuario"))).send_keys(login)
    wait.until(EC.visibility_of_element_located((By.ID, "senha"))).send_keys(senha)

    # click on the login button and verify if the login was successful
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[1]/form/div/div/div/div[4]/div/button")
        )
    ).click()

    try:
        # verifica se ID empresas está visível
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


def processar_linha_controle(browser, df, linha_inicial_controle, tentativas_login):

    site = df["Link"].iloc[linha_inicial_controle]
    login = df["LOGIN|SENHA"].iloc[linha_inicial_controle]
    senha = df["SENHA"].iloc[linha_inicial_controle]
    municipio = df["Município"].iloc[linha_inicial_controle]

    # Verifica se o login e senha já foram tentados
    if (login, senha) in tentativas_login:
        print(f"Login e senha já tentados para {site}")
        df.at[linha_inicial_controle, "Observação"] = df.at[
            linha_inicial_controle - 1, "Observação"
        ]
    else:
        try:
            browser.get(site)
            print(f"Acessando {site}...")
            browser.implicitly_wait(20)

            if "Certificado" in str(login):
                print("ACESSO POR CERTIFICADO")
                df.at[linha_inicial_controle, "Observação"] = "ACESSO POR CERTIFICADO"
            else:
                # Lidar com login (presume que a função existe)
                lidar_com_login(
                    browser, login, senha, municipio, df, linha_inicial_controle
                )
                # Registrar a tentativa de login
                tentativas_login.add((login, senha))

        except Exception as e:  # Captura a exceção específica
            print(f"Erro ao acessar {site}:")
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
    linha_inicial_controle = processar_linha_controle(
        browser, df, linha_inicial_controle, tentativas_login
    )

# Loop para testes
""" 
 while linha_inicial_controle < 25:
     linha_inicial_controle = processar_linha_controle(browser, df, linha_inicial_controle, tentativas_login)
"""
