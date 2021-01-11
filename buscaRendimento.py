import requests, bs4
from datetime import datetime


def getFIIs(arquivo):
    resFII = requests.get('https://script.google.com/macros/s/AKfycbxtvypvh4CWfOFQT0O1Xfn1DKEdAI0MSU0_1Dv7VQUN803_fww/exec')
    resFII.raise_for_status()
    arquivo.write(resFII.text+"\n")
    return resFII.text.split(',')


def atualizaValorRendimento(fii,data,valor):
    parametros = '?fii='+fii+'&date='+data+'&vlr='+valor
    url = 'https://script.google.com/macros/s/AKfycbyLFH-qPYgmr2HUrhr3P6Q_NRiGwgKV5MKuRh1GZ-2CUiGl70yr/exec'+parametros
    res = requests.get(url)
    res.raise_for_status()

def processa_response(resp,fii,arquivo):
    resp.raise_for_status()
    noStarchSoup = bs4.BeautifulSoup(resp.text,features="html.parser")
    tabela = noStarchSoup.select('#last-revenues--table')
    tbody = bs4.BeautifulSoup(str(tabela),features="html.parser")
    trs = tbody.select('tr')
    tds = trs[1].select('td')
    arquivo.write(fii+" "+tds[1].text+" "+tds[4].text+"\n")
    atualizaValorRendimento(fii,tds[1].text,tds[4].text)

def exec_busca():
    arquivo = open('resposta.log','w')
    arquivo.write("ULTIMA EXECUCAO "+datetime.now().today().strftime('%d/%m/%Y %H:%M')+"\n")
    fiis = getFIIs(arquivo)
    for fii in fiis:
        url = 'https://fiis.com.br/'+fii
        res = requests.get(url)
        processa_response(res,fii,arquivo)
    arquivo.close()

#exec_busca()






#res = requests.get('https://fiis.com.br/rbrr11/')

#res.raise_for_status()

#noStarchSoup = bs4.BeautifulSoup(res.text,features="html.parser")

#tabela = noStarchSoup.select('#last-revenues--table')
#tbody = bs4.BeautifulSoup(str(tabela),features="html.parser")
#print(tbody.select('tbody'))
#trs = tbody.select('tr')
#tds = trs[1].select('td')

#print(tds[1].text,tds[4].text)

#print(tds)

#print(trs[0].select('th'))
#print(trs[1].select('td'))
