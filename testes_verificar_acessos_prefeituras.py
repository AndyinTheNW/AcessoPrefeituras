import unittest
from VerificarAcessosPrefeituras import (
    driver,
    wait,
    df,
    ARQUIVO_CONTROLE,
    ARQUIVO_EXCEL,
    login_jundiai,  
)

class TestJundiai(unittest.TestCase):
    def test_login_jundiai(self):
        municipio_alvo = "Jundiaí"
        linha_inicial_controle = df[df["Município"] == municipio_alvo].index[0]

        with open(ARQUIVO_CONTROLE, "w") as f:
            f.write(str(linha_inicial_controle))

        login = str(df["LOGIN|SENHA"].iloc[linha_inicial_controle])
        senha = str(df["SENHA"].iloc[linha_inicial_controle])
        
        resultado_login = login_jundiai(driver, login, senha, linha_inicial_controle)

        self.assertIn(resultado_login, ["VÁLIDO", "LOGIN INVALIDO"])

if __name__ == "__main__":
    unittest.main()
