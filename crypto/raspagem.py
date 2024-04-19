# Vamos utilizar o pacote Selenium Python para manipular browsers via código:
# https://selenium-python.readthedocs.io/
#
# Para isso, ele precisa ser instalado via pip (de preferência com o VS Code fechado):
# python -m pip install selenium
#
# Depois de instalar o Selenium Python, é necessário instalar o driver referente
# ao browser que será utilizado:
#
# Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
# Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# Firefox: https://github.com/mozilla/geckodriver/releases
# Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/
#
# Depois de baixar o driver, garantir que ele seja instalado/descompactado em uma
# pasta que pertença ao PATH global do sistema (de preferência com o VS Code fechado).
#
# No Linux, podem ser as pastas /usr/bin, /usr/local/bin ou outra que esteja no PATH.
# Para adicionar outra pasta ao PATH, basta editar o arquivo ~/.bashrc, e adicionar
# uma linha parecida com essa:
# export PATH=/nova/pasta/para/adicionar:${PATH}
#
# No Windows, o PATH pode ser editado clicando com o botão direito sobre o ícone do
# Computador (no Windows Explorer), depois no menu "Propriedades", em seguida "Configurações
# avançadas do sistema" e, por fim, em "Variáveis de Ambiente".
import sys
import time
import sql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import url

def extrair_float(texto):
	try:
		i = texto.find('$')
		if i >= 0:
			texto = texto[(i + 1):]

		texto = texto.replace(',', '')

		return texto
	except:
		return 0

driver = webdriver.Chrome()
driver.get(url)

linhas = WebDriverWait(driver, 20).until(
	EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.sc-14cb040a-3 tbody tr'))
)

idleitura = sql.criarLeitura()

for linha in linhas:
	celulas = linha.find_elements(By.CSS_SELECTOR, 'td')
	try:
		nome = celulas[2].find_element(By.CSS_SELECTOR, '.kKpPOn').text
		sigla = celulas[2].find_element(By.CSS_SELECTOR, '.iqdbQL').text
		valor = extrair_float(celulas[3].text)
	except:
		spans = celulas[2].find_elements(By.CSS_SELECTOR, 'span')
		nome = spans[1].text
		sigla = spans[2].text
		valor = extrair_float(celulas[3].text)

	idcurrency = sql.obter_idcurrency(sigla)
	if idcurrency == None:
		idcurrency = sql.criarCurrency(nome, sigla)
	sql.criarRanking(idleitura, idcurrency, valor)
#print(dados)

driver.close()
