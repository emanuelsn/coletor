import xlwt 
import DB as banco


def criar_planilha():
    workbook = xlwt.Workbook()  
    sheet = workbook.add_sheet("Planilha de Testes") 
  
    # Definindo Estilo de Título 
    css_titulo = xlwt.easyxf('font: bold 1') 

    # Definindo títulos das colunas e Conteudos
    titulos = ['NOME DO PRODUTO', 'VALOR A VISTA', 'VALOR A PRAZO','CÓDIGO DE BARRAS','LINK DO PRODUTO']
    row = 0
    col = 0
    # Escrevendo títulos
    for t in titulos:
        sheet.write(row, col, t, css_titulo) 
        col= col +1
    # Recuperando dados do Banco de Dados
    cursor = banco.conectaBanco()
    sql = '''Select nomeProduto, cast(valorAVista as decimal(10,2)), cast(valorAPrazo as decimal(10,2)),codigoBarras,linkProduto from produtos'''
    cursor.execute(sql)
    retorno_bd = cursor.fetchall()

    # Definições Complementares
    row = 1
    col=0
    limite = 0

    # iterando em cada elemento retornado
    for resultado in retorno_bd:
        resultado = str(resultado).replace('\\n','').replace('(','').replace(')','').replace('\'','').split(',')
        # iterando em cada posição da lista    
        for r in resultado:
            r = str(r).replace(',','.')
            sheet.write(row,col,str(r))
            col = col+1
        # escrevendo próxima linha e voltando coluna para o início
        row = row+1
        col = 0

    # Salvando o arquivo
    nome_arquivo = 'Spartan-LojaDoProfissional.xls'
    workbook.save(nome_arquivo)
    return nome_arquivo

criar_planilha()