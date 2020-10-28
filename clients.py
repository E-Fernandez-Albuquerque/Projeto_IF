from PyQt5 import uic,QtWidgets
import pymysql

#EXIBIR TELA DE CADASTRO
def tela_cadastro():
    inicio.hide()
    telacadastro.show()


#EXIBIR TELA DE CONSULTA
def tela_consulta():
    inicio.hide()
    telaconsulta.show()


#VOLTA À TELA INICIAL
def tela_inicial_cadastro():
    inicio.show()
    telacadastro.hide()


#VOLTA À TELA INICIAL
def tela_inicial_consulta():
    inicio.show()
    telaconsulta.hide()


#PARA CADASTRAR
def cadastrar():
    cursor = banco.cursor()

    #CRIAÇÃO E SELEÇÃO DE BANCO DE DADOS, SE NÃO EXISTENTE
    cursor.execute('CREATE DATABASE IF NOT EXISTS plano_de_saude')
    cursor.execute('USE plano_de_saude')

    #CRIAÇÃO DA TABLE, SE NÃO EXISTENTE
    cursor.execute('CREATE TABLE IF NOT EXISTS clientes ('
                   'id INT AUTO_INCREMENT PRIMARY KEY, '
                   'nome VARCHAR(250) NOT NULL, '
                   'nascimento VARCHAR(20), '
                   'telefone VARCHAR(20) NOT NULL, '
                   'email VARCHAR(255) UNIQUE, '
                   'cpf VARCHAR(20) NOT NULL UNIQUE, '
                   'rg VARCHAR(20) NOT NULL UNIQUE, '
                   'plano VARCHAR(60) NOT NULL, '
                   'valor_plano VARCHAR(10) NOT NULL,'
                   'corretor VARCHAR(60) NOT NULL, '
                   'forma_pgto VARCHAR(30) NOT NULL)')

    #RECEPÇÃO DOS VALORES
    nome = telacadastro.nome_cliente.text()
    nascimento = telacadastro.nascimento.text()
    telefone = telacadastro.telefone.text()
    email = telacadastro.email.text()
    cpf = telacadastro.cpf.text()
    rg = telacadastro.rg.text()
    corretor = telacadastro.corretor.text()
    forma_pgto = telacadastro.forma_pgto.text()
    if telacadastro.plano_A.isChecked():
        plano = "Plano Prime"
        valor_plano = 'R$100'
    elif telacadastro.plano_B.isChecked():
        plano = "Plano Premium"
        valor_plano = 'R$200'
    elif telacadastro.plano_C.isChecked():
        plano = "Plano Platinum"
        valor_plano = 'R$500'

    #INSERÇÃO EM BANCO DE DADOS
    try:
        comando_SQL = 'INSERT INTO clientes (nome, nascimento, telefone, email, cpf, rg, plano, valor_plano, corretor, forma_pgto) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        dados = (nome,nascimento,telefone,email,cpf,rg,plano,valor_plano,corretor,forma_pgto)
        cursor.execute(comando_SQL, dados)
        banco.commit()
    except:
        error.show()
    else:
        sucessful.show()


#PARA CONSULTAR
def consultar():
    #RECEBIMENTO DE DADOS PARA PESQUISA
    consulta_nome = str(telaconsulta.busca_nome.text())
    consulta_cpf = str(telaconsulta.busca_cpf.text())
    consulta_rg = str(telaconsulta.busca_rg.text())

    # SELEÇÃO DE BANCO DE DADOS
    try:
        cursor = banco.cursor()
        cursor.execute('USE plano_de_saude')
        comando_SQL = f'SELECT * FROM clientes WHERE nome LIKE "%{consulta_nome}%" AND cpf LIKE "%{consulta_cpf}%" AND rg LIKE "%{consulta_rg}%"'
        cursor.execute(comando_SQL)
        retorno = cursor.fetchall()

        # CRIAÇÃO DE TABELA PARA EXIBIÇÃO DE RESULTADOS
        resultado_pesquisa.lista_resultados.setRowCount(len(retorno))
        resultado_pesquisa.lista_resultados.setColumnCount(11)
        # ESCRITA DE DADOS DO BANCO EM TABELA
        for i in range(0, len(retorno)):
            for j in range(0, 11):
                resultado_pesquisa.lista_resultados.setItem(i, j, QtWidgets.QTableWidgetItem(str(retorno[i][j])))
        # EXIBIR TABELA COM RETORNO DE BANCO DE DADOS
        resultado_pesquisa.show()
    except:
        fail_banco.show()
    else:
        print('Ok')


#FECHAMENTO DE TELA DE SUCESSO DE CADASTRO
def close_sucess():
    sucessful.hide()


#FECHAMENTO DE TELA DE ERRO
def close_error():
    error.hide()


#FECHAMENTO DE TELA DE FALHA DE ACESSO BD
def close_fail():
    fail_banco.hide()


#ABERTURA DE TELA PARA CONFIRMAR EXCLUSÃO
def solicitar_exc():
    exclusao.show()


#FUNÇÃO DE EXCLUSÃO DE BANCO DE DADOS
def excluir():
    excluir = resultado_pesquisa.lista_resultados.currentRow()
    print(excluir)
    resultado_pesquisa.lista_resultados.removeRow(excluir)

    consulta_nome = str(telaconsulta.busca_nome.text())
    consulta_cpf = str(telaconsulta.busca_cpf.text())
    consulta_rg = str(telaconsulta.busca_rg.text())

    cursor = banco.cursor()
    cursor.execute(f'SELECT id FROM clientes WHERE nome LIKE "%{consulta_nome}%" AND cpf LIKE "%{consulta_cpf}%" AND rg LIKE "%{consulta_rg}%"')
    dados_lidos = cursor.fetchall()
    dados = []
    for x in dados_lidos:
        dados.append(x[0])
        dados.sort()
    print(dados)
    id_deletar = dados[excluir]
    print(id_deletar)

    print(dados_lidos)
    #id_deletar = dados_lidos[excluir][0]
    cursor.execute("DELETE FROM clientes WHERE id=" + str(id_deletar))
    banco.commit()
    exclusao.hide()


#CANCELAR EXCLUSÃO DE DADO
def cancelar_excluir():
    exclusao.hide()


#DETALHAMENTO DE BANCO DE DADOS A SER USADO
banco = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = ''
)


#CARREGAMENTO DE INTERFACE
programa = QtWidgets.QApplication([])
inicio = uic.loadUi('Inicio.ui')
telacadastro = uic.loadUi('cadastrar.ui')
telaconsulta = uic.loadUi('consultar.ui')
exclusao = uic.loadUi('excluir.ui')
error = uic.loadUi('Erro.ui')
fail_banco = uic.loadUi('fail_banco.ui')
sucessful = uic.loadUi('Sucesso.ui')
resultado_pesquisa = uic.loadUi('consulta.ui')


#BOTOES E AÇÕES
telacadastro.btn_inicial.clicked.connect(tela_inicial_cadastro) #Tela de cadastro para inicial
telaconsulta.btn_inicial.clicked.connect(tela_inicial_consulta) #Tela de consulta para inicial
inicio.btn_cadastro.clicked.connect(tela_cadastro) #Tela de inicio para cadastro
inicio.btn_consulta.clicked.connect(tela_consulta) #Tela de inicio para consulta
telacadastro.cadastrar.clicked.connect(cadastrar) #Tentar cadastro
telaconsulta.buscar.clicked.connect(consultar) #Tentar consulta
error.ok_erro.clicked.connect(close_error) #Fechar mensagem de erro
sucessful.ok_cadastro.clicked.connect(close_sucess) #Fechar mensagem de sucesso
resultado_pesquisa.excluir.clicked.connect(solicitar_exc) #Confirma exclusão de dado
exclusao.ok_excluir.clicked.connect(excluir) #Abre a caixa de diálogo com confirmação de exclusão
exclusao.cancelar_excluir.clicked.connect(cancelar_excluir) #Cancela a exclusão de dados
fail_banco.ok_fail.clicked.connect(close_fail) #Fecha janela de erro de acesso ao banco de dados


#EXIBIÇÃO DE JANELA
inicio.show()
programa.exec()