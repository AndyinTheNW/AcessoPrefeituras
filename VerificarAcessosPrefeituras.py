from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import pyautogui as py
from twocaptcha import TwoCaptcha
import pyautogui

pyautogui.FAILSAFE = False


# Constantes
ARQUIVO_BASE = 'C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\'

ARQUIVO_CONTROLE = ARQUIVO_BASE + 'controle.txt'
ARQUIVO_EXCEL = ARQUIVO_BASE + 'ValidarAcessoPrefeituras.xlsx'
CHROME_DRIVER = ARQUIVO_BASE + 'chromedriver.exe'

with open(ARQUIVO_CONTROLE, "r") as arquivo_controle:
    linha_inicial_controle = int(arquivo_controle.read())
    print("linha arquivo controle")
    print(linha_inicial_controle)

df = pd.read_excel(ARQUIVO_EXCEL)
linha = df.shape[0]
print(linha)

emp = df['CNPJ'][3]
s = Service(executable_path=CHROME_DRIVER)

browser = webdriver.Chrome(service=s)
browser.maximize_window()

# def resolver_captcha(
#     driver, max_tentativas=1, api_key="8b05577f4418224a86a76ff3bd2b6474", captcha_xpath="/html/body/form/div[3]/div[1]/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/img"
# ):

#     if not captcha_xpath:
#         captcha_xpath = "/html/body/form/div[3]/div[1]/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/img"

#     for tentativa in range(1, max_tentativas + 1):
#         print(f"Tentativa {tentativa}: Iniciando desafio CAPTCHA...")

#         try:
#             captcha_element = driver.find_element(By.XPATH, captcha_xpath)
#             captcha_img_path = "captcha.jpg"  # Salva no diretório de trabalho atual
#             captcha_element.screenshot(captcha_img_path)
#             print("Imagem CAPTCHA salva.")

#             with TwoCaptcha(api_key) as solver:
#                 result = solver.normal(captcha_img_path)
#                 code = result["code"]

#             print(f"CAPTCHA resolvido: {code}")
#             driver.find_element(By.XPATH, '/html/body/form/div[3]/div[1]/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/div/input').send_keys(code)
#             time.sleep(2)

#             return  # Sai da função em caso de resolução bem-sucedida
#         except Exception as e:
#             print(f"Erro ao resolver CAPTCHA: {e}")

#             # Atualiza a página se restarem mais tentativas
#             if tentativa < max_tentativas:
#                 print("Atualizando página...")
#                 py.hotkey("f5")  # Usa "f5" minúsculo para PyAutoGUI
#                 time.sleep(5)

#     # Levanta uma exceção se todas as tentativas falharem
#     raise Exception(
#         "Número máximo de tentativas CAPTCHA atingido. Não foi possível resolver."
#     )


def lidar_com_login(browser, login, senha, municipio, df,linha_inicial_controle):
    status_login = ""  

    if municipio == "São Paulo":
        status_login = "ACESSO POR CERTIFICADO"
    elif municipio == "Barra Mansa":
        browser.find_element(By.ID, 'vUSUARIO_LOGIN').send_keys(login)
        browser.find_element(By.ID, 'vUSUARIO_SENHA').send_keys(senha)
        browser.find_element(By.ID, 'BTN_ENTER3').click()
        browser.implicitly_wait(10)
        y = str(linha_inicial_controle)
        try:
            browser.find_element(By.XPATH, '//*[@id="TABLECPF"]/div[2]/div').click()
            browser.implicitly_wait(50)
            print('LOGIN INVALIDOS')
            df.at[linha_inicial_controle, 'Observação'] = 'LOGIN INVALIDO'
            df.to_excel(ARQUIVO_EXCEL, index=False)
            time.sleep(3)
        except:
            print('VALIDOS')

        # Verifica se o login é inválido
        if browser.find_elements(By.XPATH, '//*[@id="TABLECPF"]/div[2]/div'):
            print('LOGINS INVÁLIDOS') 
        else:
            status_login = "VÁLIDOS"

    elif 'Jaú' in municipio:

        df.at[linha_inicial_controle, 'Observação'] = 'VERIFICAR ACESSO'
        df.to_excel(ARQUIVO_EXCEL, index=False)
        linha_inicial_controle= linha_inicial_controle+ 1
        time.sleep(3)

    elif 'Ituiutaba' in municipio:
        browser.find_element(By.ID, 'usuario').send_keys(login)
        browser.find_element(By.ID, 'senha').send_keys(senha)
        browser.find_element(By.XPATH, '//*[@id="closebuttons1btOk"]/table/tbody/tr/td[2]').click()
        browser.implicitly_wait(8)
        print('LOGIN VÁLIDO')
        status_login = "VÁLIDO"

    elif 'Betim' in municipio:
        status_login = "Verificar forma de acesso"
        linha_inicial_controle= linha_inicial_controle+ 1
        try:
            print(status_login)
        except:
            print(status_login)


    elif 'Jataí' in municipio:
        browser.find_element(By.ID, 'formLogin:log').send_keys(login)
        browser.find_element(By.ID, 'formLogin:pwd').send_keys(senha)
        browser.find_element(By.ID, 'formLogin:patternLogin').click()
        try:
            usu = browser.find_element(By.XPATH, '//*[@id="user-actions"]/div/span[2]').text
            print('LOGIN VÁLIDO')
            status_login = "VÁLIDO"
        except:
            print('LOGIN E SENHA INVALIDO')
            status_login = "LOGIN INVALIDO"

    elif 'Balneário Camboriú' in municipio:
        browser.find_element(By.ID, 'cpf').send_keys(login)
        browser.find_element(By.XPATH, '//*[@id="frmMenuExterno"]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/input').send_keys(
            senha)
        browser.find_element(By.XPATH, '//*[@id="frmMenuExterno"]/table[2]/tbody/tr/td/table/tbody/tr[4]/td/input[1]').click()
        try:
            usu = browser.find_element(By.XPATH, '//*[@id="agrupador-area"]/div[2]/table/tbody/tr/td[3]/div').text
            print('LOGIN VÁLIDO')
            status_login = "VÁLIDO"
        except:
            print('LOGIN E SENHA INVALIDO')
            status_login = "LOGIN INVALIDO"

    elif 'Jardim' in municipio:
        df.at[linha_inicial_controle, 'Observação'] = 'VERIFICAR ENDEREÇO PAGINA'
        df.to_excel(ARQUIVO_EXCEL, index=False)
        time.sleep(3)
        linha_inicial_controle= linha_inicial_controle+ 1

    elif 'Janaúba' in municipio:
        browser.find_element(By.ID, 'j_idt47:login').send_keys(login)
        browser.find_element(By.ID, 'j_idt47:senha').send_keys(senha)
        browser.find_element(By.ID, 'j_idt47:j_idt60').click()
        try:
            usu = browser.find_element(By.XPATH, '//*[@id="j_idt14:j_idt15"]/i').click()
            print('LOGIN VÁLIDO')
            status_login = "VÁLIDO"
        except:
            print('LOGIN E SENHA INVALIDO')
            status_login = "LOGIN INVALIDO"

    elif 'Américo Brasiliense' in municipio:
        df.at[linha_inicial_controle, 'Observação'] = 'FALTA INFORMAÇÃO'
        df.to_excel(ARQUIVO_EXCEL, index=False)
        time.sleep(3)
        linha_inicial_controle= linha_inicial_controle+ 1

    elif 'Birigui' in municipio:
        df.at[linha_inicial_controle, 'Observação'] = 'VERIFICAR ACESSO'
        df.to_excel(ARQUIVO_EXCEL, index=False)
        time.sleep(3)
        linha_inicial_controle= linha_inicial_controle+ 1

    elif 'Açailândia' in municipio or 'Barretos' in municipio:
        df.at[linha_inicial_controle, 'Observação'] = 'VERIFICAR ACESSO'
        df.to_excel(ARQUIVO_EXCEL, index=False)
        time.sleep(3)
        linha_inicial_controle= linha_inicial_controle+ 1

    elif 'Altamira' in municipio:
        browser.find_element(By.ID, 'login-cnpj-tab').click()
        browser.find_element(By.ID, 'usuarioCnpj').click()
        browser.find_element(By.ID, 'usuarioCnpj').send_keys(login)
        browser.find_element(By.ID, 'senhaCnpj').send_keys(senha)
        browser.find_element(By.ID, 'botaoCapcthaCnpj').click()
        try:
            usu = browser.find_element(By.XPATH, '//*[@id="menu-button"]/i').click()
            print('LOGIN VÁLIDO')
            status_login = "VÁLIDO"
        except:
            print('LOGIN E SENHA INVALIDO')
            status_login = "LOGIN INVALIDO"

    elif 'Barreiras' in municipio or 'Jequié' in municipio:
        browser.find_element(By.ID, 'usuario').send_keys(login)
        browser.find_element(By.ID, 'senha').send_keys(senha)
        browser.find_element(By.XPATH, '/html/body/div/main/div/div/div/div[1]/form/div[4]/span/button').click()
        try:
            usu = browser.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div/div[1]/form/div[2]/div/div/div').text
            print('LOGIN VÁLIDO')
            status_login = "VÁLIDO"
        except:
            print('LOGIN E SENHA INVALIDO')
            status_login = "LOGIN INVALIDO"

    elif 'Belo Horizonte' in municipio:
        browser.find_element(By.XPATH, '//*[@id="form"]/div[2]/a/img').click()
        browser.find_element(By.ID, 'username').send_keys(login)
        browser.find_element(By.ID, 'password').send_keys(senha)
        browser.find_element(By.XPATH, '//*[@id="fm1"]/div[3]/button').click()
        try:
            usu = browser.find_element(By.XPATH, '//*[@id="identificacao"]/table/tbody/tr/td[2]/a').click()
            print('LOGIN VÁLIDO')
            status_login = "VÁLIDO"
        except:
            print('LOGIN E SENHA INVALIDO')
            status_login = "LOGIN INVALIDO"
            

#  Rio de janeiro incompleto
    elif 'Rio de Janeiro' in municipio:
        browser.find_element(By.ID, 'ctl00_cphCabMenu_tbCpfCnpj').send_keys(login)
        browser.find_element(By.ID, 'ctl00_cphCabMenu_tbSenha').send_keys(senha)
        time.sleep(3)
        # resolver_captcha(browser)
        # print("captcha resolvido")
        time.sleep(3)
        browser.find_element(By.XPATH , '/html/body/form/div[3]/div[1]/div[6]/div/div/div[2]/div[1]/div[2]/input').click()
        time.sleep(3)

        #ctl00_cphCabMenu_vsErros

        if browser.find_elements(By.ID, 'ctl00_cphCabMenu_vsErros'):
            print('LOGIN E SENHA INVALIDO')
            status_login = "LOGIN INVALIDO"
        else:
            print('LOGIN VÁLIDO')
            status_login = "VÁLIDO"

        # try:
        #     usu = browser.find_element(By.XPATH, '').click()
        #     print('LOGIN VÁLIDO')
        #     status_login = "VÁLIDO"
        # except:
        #     print('LOGIN E SENHA INVALIDO')
        #     status_login = "LOGIN INVALIDO"

    df.at[linha_inicial_controle, 'Observação'] = status_login
    df.to_excel(ARQUIVO_EXCEL, index=False)

    # VERIFICA SE OS DADOS DE ACESSO JÁ FORAM VERIFICADOS

    for i in range(linha_inicial_controle):
        if login == df['LOGIN|SENHA'][i] and senha == df['SENHA'][i]:
            print("Dados de acesso já verificados. Pulando para a próxima linha...")
            df.at[linha_inicial_controle, 'Observação'] = df['Observação'][i]
            df.to_excel(ARQUIVO_EXCEL, index=False)
            time.sleep(3)
            linha_inicial_controle+= 1
            continue
    

# Loop principal
with open(ARQUIVO_CONTROLE, "r") as arquivo_controle:
    linha_inicial_controle= int(arquivo_controle.read())  


while linha_inicial_controle < 20:
    site = df['Link'][linha_inicial_controle]
    login = df['LOGIN|SENHA'][linha_inicial_controle]
    senha = df['SENHA'][linha_inicial_controle]
    municipio = df['Município'][linha_inicial_controle]


# Verifica se os dados de acesso já foram verificados
    

    # linha_anterior_planilha = df.iloc[linha_inicial_controle - 1] if linha_inicial_controle > 0 else None

    # if linha_anterior_planilha is not None and linha_anterior_planilha['LOGIN|SENHA'] == login and linha_anterior_planilha['SENHA'] == senha:
    #     print("Dados de acesso já verificados. Pulando para a próxima linha...")
    #     df.at[linha_inicial_controle, 'Observação'] = linha_anterior_planilha['Observação']

    print(login, site, sep="\n")

    try:
        browser.get(site)
        browser.implicitly_wait(10)
    except:
        df.at[linha_inicial_controle, 'Observação'] = 'PÁGINA NÃO ABRIU'
        df.to_excel(ARQUIVO_EXCEL, index=False)
        time.sleep(3)
        linha_inicial_controle+= 1
        continue
    
    if 'Certificado' in str(login):
        print("ACESSO POR CERTIFICADO")
        df.at[linha_inicial_controle, 'Observação'] = 'ACESSO POR CERTIFICADO'
        df.to_excel(ARQUIVO_EXCEL, index=False)
    else:
        lidar_com_login(browser, login, senha, municipio, df, linha_inicial_controle,)


    time.sleep(3)
    linha_inicial_controle += 1

    # Salva o progresso após cada iteração
    with open(ARQUIVO_CONTROLE, "w") as f:
        f.write(str(linha_inicial_controle))


print('FIM')

with open(ARQUIVO_CONTROLE, "w") as f:
    f.write("0") 

browser.quit()







