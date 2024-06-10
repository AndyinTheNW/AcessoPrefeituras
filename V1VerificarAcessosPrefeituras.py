from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import xlrd
import openpyxl


inicia = open(r"C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\Controle.txt", "r")
linha_inicia = inicia.read()
print("linha arquivo controle")
print(linha_inicia)
x = int(linha_inicia)
print(x)
inicia.close()

df = pd.read_excel(r'C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx')
linha = df.shape[0]
print(linha)

emp = df['CNPJ'][3]
s = Service(executable_path=r"C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\chromedriver.exe")

browser = webdriver.Chrome(service=s)

browser.maximize_window()

while x < 20:
#---------colocar aqui  o if para identificar se municipio se repete

    obs = df['Observação'][x]
    if obs == "" or obs == 'nan':
        print('Processeguir')
    else:
        login = df['LOGIN|SENHA'][x]
        senha = df['SENHA'][x]
        y = x - 1
        login1 = df['LOGIN|SENHA'][y]
        senha1 = df['SENHA'][y]
        if login == login1 and senha == senha1:
            df.at[x, 'Observação'] = obs
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx',
                        index=False)
            time.sleep(3)
            x = x + 1
            continue


#----------------------------------------------------------------
    site = df['Link'][x]
    login = df['LOGIN|SENHA'][x]
    senha = df['SENHA'][x]
    municipio = df['Município'][x]
    print(login)
    print(site)

    print('________________________________________________________________-_____')
    print(x)
    try:
        browser.get(site)
        browser.implicitly_wait(10)
    except:
        df.at[x, 'Observação'] = 'PAGINA NÃO ABRIU'
        df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
        time.sleep(3)
        x = x + 1
        continue

    print('_________________________________________________________________________')

    if 'Certificado' in str(login):
        print('ACESSO POR CERTIFICADO')

    if 'São Paulo' in municipio:
        df.at[x, 'Observação'] = 'ACESSO POR CERTIFICADO'
        df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
        time.sleep(3)
        x = x + 1
        continue

    elif 'Barra Mansa' in municipio:
        # print(browser.page_source)
        # //*[@id="CONTAINERCAMPOS"]/div[2]/div
        # browser.find_element_by_xpath('//*[@id="CONTAINERCAMPOS"]/div[2]/div').click()
        # vUSUARIO_LOGIN

        browser.find_element(By.ID, 'vUSUARIO_LOGIN').send_keys(login)
        browser.implicitly_wait(15)

        browser.find_element(By.ID, 'vUSUARIO_SENHA').send_keys(senha)
        browser.implicitly_wait(10)

        browser.find_element(By.ID, 'BTN_ENTER3').click()
        browser.implicitly_wait(10)
        y = str(x)
        try:
            browser.find_element(By.XPATH, '//*[@id="TABLECPF"]/div[2]/div').click()
            browser.implicitly_wait(50)
            print('LOGIN INVALIDOS')
            df.at[x, 'Observação'] = 'LOGIN INVALIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
        except:
            print('VALIDOS')

    elif 'Jaú' in municipio:

        df.at[x, 'Observação'] = 'VERIFICAR ACESSO'
        df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
        x = x + 1
        time.sleep(3)
        continue

    elif 'Ituiutaba' in municipio:
        # usuario
        # senha
        # //*[@id="closebuttons1btOk"]/table/tbody/tr/td[2]
        browser.find_element(By.ID, 'usuario').send_keys(login)
        browser.implicitly_wait(15)

        browser.find_element(By.ID, 'senha').send_keys(senha)
        browser.implicitly_wait(10)
        time.sleep(1)

        browser.find_element(By.XPATH, '//*[@id="closebuttons1btOk"]/table/tbody/tr/td[2]').click()
        browser.implicitly_wait(10)

        print(login)
        print(senha)
        time.sleep(1)
        try:
            browser.find_element(By.ID, '_CBoImgCancel').click()
            browser.implicitly_wait(8)
            print('LOGIN VÁLIDO')
            df.at[x, 'Observação'] = 'VÁLIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
        except:
            print('LOGIN E SENHA INVALIDO')
            df.at[x, 'Observação'] = 'LOGIN INVALIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
        # _CBoImgCancel
        # Betim

    elif 'Betim' in municipio:

        df.at[x, 'Observação'] = 'VERIFICAR ACESSO'
        df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
        x = x + 1
        time.sleep(3)
        continue

    # formLogin:log
    # formLogin:pwd
    # formLogin:patternLogin
    elif 'Jataí' in municipio:

        browser.find_element(By.ID, 'formLogin:log').send_keys(login)
        browser.implicitly_wait(15)

        browser.find_element(By.ID, 'formLogin:pwd').send_keys(senha)
        browser.implicitly_wait(10)
        time.sleep(1)

        browser.find_element(By.ID, 'formLogin:patternLogin').click()
        browser.implicitly_wait(10)

        print(login)
        print(senha)
        time.sleep(1)

        try:
            usu = browser.find_element(By.XPATH, '//*[@id="user-actions"]/div/span[2]').text
            browser.implicitly_wait(10)
            print('LOGIN VÁLIDO')
            df.at[x, 'Observação'] = 'VÁLIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
        except:
            print('LOGIN E SENHA INVALIDO')
            df.at[x, 'Observação'] = 'LOGIN INVALIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)


    elif 'Balneário Camboriú' in municipio:

        browser.find_element(By.ID, 'cpf').send_keys(login)
        browser.implicitly_wait(15)

        browser.find_element(By.XPATH,
                             '//*[@id="frmMenuExterno"]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/input').send_keys(
            senha)
        browser.implicitly_wait(10)
        time.sleep(1)

        browser.find_element(By.XPATH,
                             '//*[@id="frmMenuExterno"]/table[2]/tbody/tr/td/table/tbody/tr[4]/td/input[1]').click()
        browser.implicitly_wait(10)

        print(login)
        print(senha)
        time.sleep(1)
        try:
            usu = browser.find_element(By.XPATH, '//*[@id="agrupador-area"]/div[2]/table/tbody/tr/td[3]/div').text
            browser.implicitly_wait(8)
            print('LOGIN VÁLIDO')
            df.at[x, 'Observação'] = 'VÁLIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
        except:
            print('LOGIN E SENHA INVALIDO')
            df.at[x, 'Observação'] = 'LOGIN INVALIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)


    elif 'Jardim' in municipio:
        df.at[x, 'Observação'] = 'VERIFICAR ENDEREÇO PAGINA'
        df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
        time.sleep(3)
        x = x + 1
        continue

    elif 'Janaúba' in municipio:
        # j_idt47:login
        # j_idt47:senha
        # j_idt47:j_idt60
        # //*[@id="layout-topbar-menu"]/li[7]/a
        browser.find_element(By.ID, 'j_idt47:login').send_keys(login)
        browser.implicitly_wait(15)

        browser.find_element(By.ID, 'j_idt47:senha').send_keys(senha)
        browser.implicitly_wait(10)
        time.sleep(1)

        browser.find_element(By.ID, 'j_idt47:j_idt60').click()
        browser.implicitly_wait(10)

        print(login)
        print(senha)
        time.sleep(1)
        try:
            usu = browser.find_element(By.XPATH, '//*[@id="j_idt14:j_idt15"]/i').click()
            browser.implicitly_wait(10)
            print('LOGIN VÁLIDO')
            df.at[x, 'Observação'] = 'VÁLIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
        except:
            print('LOGIN E SENHA INVALIDO')
            df.at[x, 'Observação'] = 'LOGIN INVALIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)

    elif 'Américo Brasiliense' in municipio:
        df.at[x, 'Observação'] = 'FALTA INFORMAÇÃO'
        df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
        time.sleep(3)
        x = x + 1
        continue

    elif 'Birigui' in municipio:
        df.at[x, 'Observação'] = 'VERIFICAR ACESSO'
        df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
        time.sleep(3)
        x = x + 1
        continue

    elif 'Açailândia' in municipio or 'Barretos' in municipio:
        df.at[x, 'Observação'] = 'VERIFICAR ACESSO'
        df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
        time.sleep(3)
        x = x + 1
        continue

        # Altamira
    elif 'Altamira' in municipio:
        # usuariocpf
        # senhaCpf
        # botaoCapctha
        # //*[@id="login-cpf-tab"]
        browser.find_element(By.ID, 'login-cnpj-tab').click()
        browser.implicitly_wait(15)

        browser.find_element(By.ID, 'usuarioCnpj').click()
        browser.implicitly_wait(10)
        browser.find_element(By.ID, 'usuarioCnpj').send_keys(login)
        browser.implicitly_wait(15)

        browser.find_element(By.ID, 'senhaCnpj').send_keys(senha)
        browser.implicitly_wait(10)
        time.sleep(1)

        browser.find_element(By.ID, 'botaoCapcthaCnpj').click()
        browser.implicitly_wait(10)

        # //*[@id="menu-button"]/i
        try:
            usu = browser.find_element(By.XPATH, '//*[@id="menu-button"]/i').click()
            browser.implicitly_wait(10)
            print('LOGIN VÁLIDO')
            df.at[x, 'Observação'] = 'VÁLIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
        except:
            print('LOGIN E SENHA INVALIDO')
            df.at[x, 'Observação'] = 'LOGIN INVALIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
    # usuario
    # senha
    # //*[@id="app"]/main/div/div/div/div[1]/form/div[4]/span/button
    # //*[@id="app"]/main/div/div/div/div[1]/form/div[2]/div/div/div
    # Altamira
    elif 'Barreiras' in municipio or 'Jequié' in municipio:

        browser.find_element(By.ID, 'usuario').send_keys(login)
        browser.implicitly_wait(15)

        browser.find_element(By.ID, 'senha').send_keys(senha)
        browser.implicitly_wait(10)
        time.sleep(1)

        browser.find_element(By.XPATH, '/html/body/div/main/div/div/div/div[1]/form/div[4]/span/button').click()
        browser.implicitly_wait(15)

        # //*[@id="menu-button"]/i
        try:
            usu = browser.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div/div[1]/form/div[2]/div/div/div').text
            browser.implicitly_wait(10)
            print('LOGIN VÁLIDO')
            df.at[x, 'Observação'] = 'LOGIN INVALIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
        except:
            print('LOGIN E SENHA INVALIDO')
            df.at[x, 'Observação'] = 'VALIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
    # cpf
    # senha
    # //*[@id="frmMenuExterno"]/table[2]/tbody/tr/td/table/tbody/tr[4]/td/input[1]
    # //*[@id="agrupador-area"]/div[2]/table/tbody/tr/td[3]/div

    elif 'Belo Horizonte' in municipio:

        browser.find_element(By.XPATH, '//*[@id="form"]/div[2]/a/img').click()
        browser.implicitly_wait(15)

        browser.find_element(By.ID, 'username').send_keys(login)
        browser.implicitly_wait(15)

        browser.find_element(By.ID, 'password').send_keys(senha)
        browser.implicitly_wait(10)
        time.sleep(1)

        browser.find_element(By.XPATH, '//*[@id="fm1"]/div[3]/button').click()
        browser.implicitly_wait(10)

        try:
            usu = browser.find_element(By.XPATH, '//*[@id="identificacao"]/table/tbody/tr/td[2]/a').click()
            browser.implicitly_wait(10)
            print('LOGIN VÁLIDO')
            df.at[x, 'Observação'] = 'VÁLIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
        except:
            print('LOGIN E SENHA INVALIDO')
            df.at[x, 'Observação'] = 'LOGIN INVALIDO'
            df.to_excel('C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\ValidarAcessoPrefeituras.xlsx', index=False)
            time.sleep(3)
    # //*[@id="form"]/div[2]/a/img
    # username
    # password
    # //*[@id="fm1"]/div[3]/button
    # //*[@id="identificacao"]/table/tbody/tr/td[2]/a

    # ----------------------------------------------------------------------
    time.sleep(3)
    file = open(r"C:\\Users\\dijalma.junior\\Desktop\\AcessoPrefeituras\\Controle.txt", "w+")
    file.write(str(x))
    file.close()
    x = x + 1
print('FIM')







