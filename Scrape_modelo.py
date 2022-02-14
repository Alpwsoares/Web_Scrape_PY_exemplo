from selenium import webdriver
from pathlib import Path
import csv
import pandas as pd
from bs4 import BeautifulSoup
import time

DRIVER_PATH = str(Path('geckodriver.exe').resolve())
driver = webdriver.Firefox(executable_path=DRIVER_PATH)

def get_html(url):
    driver.get(url)
    return driver.page_source
    
def write_csv(ads):
    with open('arquivo_onde_sera_atualizado.csv', 'a', newline = '') as f:
        fields = ['data', 'titulo', 'texto', 'link do card']

        writer = csv.DictWriter(f, fieldnames = fields)

        for ad in ads:
            writer.writerow(ad)

def pandas_csv(ads, pri, ult, arq):
    df = pd.DataFrame(ads)
    df.to_csv(f'nomearquivo-{arq}-{pri}-{ult}-pd.csv', sep=';', mode='w+', encoding='utf-16', index=False)

def scrape_formatacao(card, data):
    try:
        tds = card.find_all('tipo da marcação', class_ = 'nome dos cards a serem encontrados')
    except:
        data = ''
        titulo = ''
        texto = ''
        url = ''
    else:
        data = data
        titulo = tds[0].a.text.replace('\n', '').upper()
        texto = tds[1].text.replace('\n', '').upper()
        url = tds[0].a.get('href')

    dt = {'data': data, 'titulo': titulo, 'texto': texto, 'Url': url}

    return dt


def _scrape():
    # a busca é feita de um ano ou página inicial em sites com padronagens estruturais
    # Exemplos: sites com noticias, sites de compras, sites com várias tabelas...
    arq = 'nomeprincipal'
    pri=int(input('qual a data/ inicial para busca:'))
    ult=int(input('qual a data final para busca:'))
    ini = pri -1
    fim = ult +1
    ads_dt = []
    for i in range(ini, fim):
        url = f'http://www.site.principal/complemento/.../{i}/complemento'# é subistituido o ano ou página a cada repetição do laço
        html = get_html(url)# site é capturado
        time.sleep(1)

        soup = BeautifulSoup(html, 'lxml')# texto é estruturado com suas tags para assim ocorrer as separações 
    
        cards = soup.find_all('tr',{'class':'visaoQuadrosTr'})# escolhe uma categoria para filtrar 

        print(len(cards))

        #em cada card de todos filtrados selecionamos pontos que queremos de informação
        for card in cards[1:]:    
            dt = scrape_formatacao(card, i)#envia os dados para formatacao junto com a a numeração do ano ou página que foi estraido 
            ads_dt.append(dt)

    pandas_csv(ads_dt, pri, ult, arq)# enviar dados para gerar arquivo tabelado


def main():
    #programações principais podem ser feitas aqui
    _scrape()# chama a função para scrape


if __name__ == '__main__':

    main()