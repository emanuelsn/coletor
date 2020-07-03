# -*- coding: utf-8 -*-


import yagmail

def envio_email(mensagem, nome_planilha):
    mensagem_final = """
     Olá!, Lucas! \\n<br> 
    Estou enviando uma versão BETA dos dados que o robô-coletor encontrou hoje.<br>
    O robô-coletor fez a pesquisa por produtos do fornecedor SPARTAN no e-commerce da Loja do Profissional
    Em anexo estou enviando uma planilha com os dados.
    Nela estão disponíveis os seguintes dados:<br>
    <ul>
    <li>Descrição do Produto
    <li>Valor a Vista
    <li>Valor a Prazo
    <li>Código de Barras
    <li>Link da página do produto
    <ul\> <br>

    <p>Por ser uma versão beta, este serviço de coleta (e também o de envio de email) ainda será atualizado e melhorado algumas vezes!

    Att,
    Robô-Coletor

    """
    path_planilha = 'D:\\estudos\\selenium\\'+nome_planilha
    yag = yagmail.SMTP('emanuelsn@gmail.com', '#Emanuel1234')
    yag.send(to = 'lucmg99@gmail.com', subject ='[Versão Beta] Coleta concluída!', contents = mensagem_final,  attachments = path_planilha )