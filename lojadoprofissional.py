from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from parsel import Selector
import math
import scripts.DB as banco
import scripts.gerar_excel as excel
import scripts.envio_email as email
#Gera páginas a serem acessadas
def gera_paginas(url,quantidade):
    start = 1
    paginas = []
    while start <= quantidade:
        paginacompleta = '{0}{1}{2}'.format(url,'&pagina=',start)
        print(paginacompleta)
        paginas.append(paginacompleta)
        start = start+1
    return paginas
#Acessa a página do produto.
def acessar_pagina_produto(url):
    sleep(2)
    driver.get(url)
    sleep(4)


    ###############
    #Coletar dados
    ###############

    #Nome do Produto
    nome_produto = driver.find_element_by_xpath('/html/body/section/div/h1')
    nome_produto = nome_produto.text
    nome_produto = str(nome_produto).split('cód:')
    nome_produto = nome_produto[0]
    nome_produto = nome_produto.replace('\\n','').replace(',','')
    print(nome_produto)

    #Valor a vista
    a_vista_valor_temp = driver.find_element_by_xpath('/html/body/section/div/div[4]/div[4]/div[3]/span[1]')
    a_vista_valor_temp = str(a_vista_valor_temp.text).split(' ')
    a_vista_valor = float(a_vista_valor_temp[1].replace('.','').replace(',','.'))
    print("Vr.A vista: "+str(a_vista_valor))
    
    #Valor a prazo
    try:
        a_prazo_parcelas = driver.find_element_by_xpath('/html/body/section/div/div[4]/div[4]/div[4]/b/span')
        a_prazo_valor = driver.find_element_by_xpath('/html/body/section/div/div[4]/div[4]/div[4]/span')
        a_prazo_parcelas = int(a_prazo_parcelas.text)
        a_prazo_valor = str(a_prazo_valor.text).split(' ')
        a_prazo_valor = float(a_prazo_valor[1].replace('.','').replace(',','.'))
        a_prazo_final = a_prazo_valor * a_prazo_parcelas
        print("vr.A Prazo: "+str(a_prazo_final))
    except NoSuchElementException:
        a_prazo_final = 0.00  

    #Descrição
    descricao = driver.find_elements_by_xpath('/html/body/section/div/div[6]/p')
    desc = []
    for d in descricao:
        desc.append(d.text)
    descricao_final = ' '.join(desc)
    descricao_final = descricao_final.split('Qualidade:')
    descricao_final = str(descricao_final[0])

    #CodigoBarras
    codigo_barras = driver.find_element_by_xpath('//*[@id="ctrEscolheTamanho"]/li/a').get_attribute('ean')
    print('Codigo de Barras: '+str(codigo_barras))
    
    #LinkProduto
    linkProduto = str(url)
  

    #Monta Tupla para inserir no Banco de Dados
    produto = (nome_produto,a_vista_valor, a_prazo_final, descricao_final, linkProduto, codigo_barras)

    #Insert no Banco de Dados
    banco.insert_produto(produto)

    #Coleta dados de produtos Relacionados
    try:
        produtos_relacionados = driver.find_elements_by_xpath('/html/body/section/div/article/div/div[2]/ul/li/div[1]')
        produtos_relacionados = [relacionados.get_attribute('title') for relacionados in produtos_relacionados]
        print('\n PRODUTOS RELACIONADOS: \n')
        for relacionado in produtos_relacionados:
            print(relacionado)
            produtoRelacionado = (nome_produto,relacionado)
            banco.insert_produto_relacionado(produtoRelacionado)
    except NoSuchElementException:
        pass

############################################################
#########################  INÍCIO  #########################
############################################################


url_start = 'https://www.lojadoprofissional.com.br/'
# Chrome diver
driver = webdriver.Chrome('./chromedriver')

# maximizar janela
# driver.maximize_window()

driver.get(url_start)
sleep(3)

#localizar busca
buscador = driver.find_element_by_xpath('//*[@id="instantSearch"]')
buscador.click()
sleep(2)
pesquisa = 'SPARTAN'
buscador.send_keys(pesquisa)
print(buscador)
buscador.send_keys(Keys.RETURN)
sleep(5)

#URL pesquisa
url_pagina = driver.current_url


#Quantidade de Páginas de produtos
quantidade_pags = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/span')
quantidade_pags = str(quantidade_pags.text).split(' ')
quantidade_pags = quantidade_pags[0]
quantidade_pags = int(quantidade_pags)/24 
quantidade_pags= math.ceil(quantidade_pags)
paginas_navegadas = 1
paginas = gera_paginas(url_pagina,quantidade_pags)

for pag in paginas:
    driver.get(pag)   
    sleep(5)
    links = driver.find_elements_by_xpath('/html/body/div[3]/div[1]/div[3]/div[3]/ul/li/div/div[3]/a[2]')
    links = [link.get_attribute('href') for link in links]
    #Acessar as páginas dos produtos.
    for link in links:
        acessar_pagina_produto(link)

driver.close()    
arquivo = excel.criar_planilha()
envio = email.envio_email('Envio',arquivo)

