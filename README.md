# ValidarAcessoPrefeituras - Validador automatizado de acesso

Esse projeto Python foi desenvolvido para automatizar a validação de credenciais de login (CNPJ/CPF e senhas) para acesso a sistemas on-line de vários municípios brasileiros. O script interage com páginas da Web, resolve CAPTCHAs e registra os resultados em uma planilha do Excel.

## Visão geral do projeto

Muitas prefeituras no Brasil oferecem sistemas on-line para empresas e indivíduos acessarem informações fiscais, licenças e outros serviços. Esse projeto simplifica o processo de verificar se as credenciais de login são válidas ou inválidas.

## Como funciona

1. **Entrada de dados:**
   - Um arquivo Excel (`ValidarAcessoPrefeituras.xlsx`) contém CNPJ/CPF, senhas, nomes de municípios e links de sites correspondentes.
   - Um arquivo de controle (`controle.txt`) acompanha o progresso do script, armazenando a próxima linha a ser processada.

2. **Automação do navegador:**
   - O Selenium WebDriver controla um navegador Chrome para interagir com os sites.
   - O script navega para cada site, insere as credenciais de login e tenta fazer o login.
   - Os CAPTCHAs são manipulados usando o serviço 2Captcha.

3. **Validação e registro:**
   - O script verifica se o login foi bem-sucedido ou não.
   - Os logins bem-sucedidos são marcados como "VÁLIDO".
   - Os logins malsucedidos são marcados com o motivo da falha (por exemplo, "LOGIN INVÁLIDO", "ACESSO POR CERTIFICADO").
   - Todos os resultados são registrados no arquivo do Excel.

## Dependências

- Python:** Instalar o Python 3.x.
- Bibliotecas:** Instale as bibliotecas necessárias:
   ```bash
   pip install selenium pandas numpy pyautogui twocaptcha psutil
