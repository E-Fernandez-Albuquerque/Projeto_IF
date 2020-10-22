from PyQt5 import uic,QtWidgets
import pymysql

#FUNÇÃO PARA BOTÃO DE CADASTRO
def cadastrar():
    cursor = banco.cursor()

    #CRIAÇÃO E SELEÇÃO DE BANCO DE DADOS, SE NÃO EXISTENTE
    cursor.execute('CREATE DATABASE IF NOT EXISTS plano_de_saude')
    cursor.execute('USE plano_de_saude')

    #CRIAÇÃO DA TABLE, SE NÃO EXISTENTE
    cursor.execute('CREATE TABLE IF NOT EXISTS clientes ('
                   'nome VARCHAR(250) NOT NULL, '
                   'nascimento VARCHAR(20), '
                   'telefone VARCHAR(20) NOT NULL, '
                   'email VARCHAR(255) UNIQUE, '
                   'cpf VARCHAR(20) NOT NULL PRIMARY KEY, '
                   'rg VARCHAR(20) NOT NULL UNIQUE, '
                   'plano VARCHAR(60) NOT NULL, '
                   'valor_plano VARCHAR(10) NOT NULL,'
                   'corretor VARCHAR(60) NOT NULL, '
                   'forma_pgto VARCHAR(30) NOT NULL)')

    #RECEPÇÃO DOS VALORES
    nome = software.nome_cliente.text()
    nascimento = software.nascimento.text()
    telefone = software.telefone.text()
    email = software.email.text()
    cpf = software.cpf.text()
    rg = software.rg.text()
    corretor = software.corretor.text()
    forma_pgto = software.forma_pgto.text()
    if software.plano_A.isChecked():
        plano = "Plano Prime"
        valor_plano = 'R$100'
    elif software.plano_B.isChecked():
        plano = "Plano Premium"
        valor_plano = 'R$200'
    elif software.plano_C.isChecked():
        plano = "Plano Platinum"
        valor_plano = 'R$500'

    #INSERÇÃO EM BANCO DE DADOS
    try:
        comando_SQL = 'INSERT INTO clientes (nome, nascimento, telefone, email, cpf, rg, plano, valor_plano, corretor, forma_pgto) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        dados = (str(nome),str(nascimento),str(telefone),str(email),str(cpf),str(rg),str(plano),str(valor_plano),str(corretor),str(forma_pgto))
        cursor.execute(comando_SQL, dados)
        banco.commit()
    except:
        error.show()
    else:
        sucessful.show()


#FUNÇÃO PARA BOTÃO DE CONSULTA
def consultar():
    #RECEBIMENTO DE DADOS PARA PESQUISA
    consulta_nome = str(software.busca_nome.text())
    consulta_cpf = str(software.busca_cpf.text())
    consulta_rg = str(software.busca_rg.text())
    cursor = banco.cursor()

    # SELEÇÃO DE BANCO DE DADOS
    cursor.execute('USE plano_de_saude')
    comando_SQL = f'SELECT * FROM clientes WHERE nome LIKE "%{consulta_nome}%" AND cpf LIKE "%{consulta_cpf}%" AND rg LIKE "%{consulta_rg}%"'
    cursor.execute(comando_SQL)
    retorno = cursor.fetchall()

    #CRIAÇÃO DE TABELA PARA EXIBIÇÃO DE RESULTADOS
    resultado_pesquisa.lista_resultados.setRowCount(len(retorno))
    resultado_pesquisa.lista_resultados.setColumnCount(10)
    #ESCRITA DE DADOS DO BANCO EM TABELA
    for i in range(0,len(retorno)):
        for j in range(0,10):
            resultado_pesquisa.lista_resultados.setItem(i,j,QtWidgets.QTableWidgetItem(str(retorno[i][j])))
    #EXIBIR TABELA COM RETORNO DE BANCO DE DADOS
    resultado_pesquisa.show()

#DETALHAMENTO DE BANCO DE DADOS A SER USADO
banco = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = ''
)

#FECHAMENTO DE TELA DE SUCESSO DE CADASTRO
def close_sucess():
    sucessful.hide()


def close_error():
    error.hide()

#CARREGAMENTO DE INTERFACE
programa = QtWidgets.QApplication([])
software = uic.loadUi('Clients.ui')
error = uic.loadUi('Erro.ui')
sucessful = uic.loadUi('Sucesso.ui')
resultado_pesquisa = uic.loadUi('consulta.ui')

#BOTOES E AÇÕES
software.cadastrar.clicked.connect(cadastrar)
software.buscar.clicked.connect(consultar)
error.ok_erro.clicked.connect(close_error)
sucessful.ok_cadastro.clicked.connect(close_sucess)

#EXIBIÇÃO DE JANELA
software.show()
programa.exec()