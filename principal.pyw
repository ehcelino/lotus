# from tkinter import DISABLED
# from turtle import update
# import subprocess
import PySimpleGUI as sg
import sqlite3
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import os
import re
import shutil
import locale
import operator
import calendar
import logging
import datetime as dtt
from time import strptime
# import pygogo as py
# import random

# from PySimpleGUI import TABLE_SELECT_MODE_BROWSE

import contabil
import cores
# from colorama import Back
# from requests import NullHandler
# from tkhtmlview import *
# from fpdf import FPDF
import pdfgen

# import pandas as pd

################################################################
# OBSERVACAO: PARA O FPDF FUNCIONAR, EXECUTE EM UM CMD ELEVADO:
# setx /M SYSTEM_TTFFONTS C:\Windows\fonts
# INVALIDO: COPIE AS FONTES PARA A PASTA DO PROGRAMA
################################################################

################################################################
# PARA GERAR O EXECUTAVEL:
# pyinstaller principal.spec
################################################################

################################################################
# PROGRAMA DE GERENCIAMENTO DE ALUNOS LOTUS
#
# A FAZER
#
# RELATORIO DE PAGAMENTOS - CORRIGIR VALORES E TIRAR COR DA TABELA
# LIMPAR A TABELA DO LADO DIREITO APOS RECEBER MENSALIDADE - TALVEZ NAO
# CRIAR MENSALIDADES DESDE A DATA DE MATRICULA <----------- MUITO IMPORTANTE - TALVEZ NAO
# VERIFICAR SE ESTAO SENDO CRIADAS MENSALIDADES PARA ALUNOS INATIVOS - APARENTEMENTE NAO
# BACKUPS PARECEM FUNCIONAR OK, PRECISA DE MAIS TESTES
# OK - QUANDO APAGA O ALUNO ELE NAO E APAGADO, E SIM MARCADO COMO INATIVO
# OK - NAO ESTAO - VERIFICAR SE ALUNOS INATIVOS ESTAO ENTRANDO NOS RELATORIOS DE MENSALIDADES DEVIDAS
# OK - ESTAO - VERIFICAR SE OS VALORES DOS ALUNOS INATIVOS ESTAO ENTRANDO NOS REL. DE MENS. RECEBIDA
# PARECE OK - planos_escreve ESTA COM UM PROBLEMA SERIO NA GERACAO DE MESES, VERIFICAR OUTRO PROG PARA SOLUCAO
# OK CRIAR MENSALIDADE - FAZER CHECAGEM SE A MENSALIDADE EXISTE ANTES
# OK - VER POR QUE NAO ESTAO SENDO COLORIDOS OS ALUNOS INATIVOS
# OK VERIFICAR BACKUP COMPLETO, FAZENDO O BKP DO LUGAR ERRADO CRIANDO ARQUIVO ENORME
# OK CORES NA TABELA PRINCIPAL NAO ESTAO FUNCIONANDO <---------------------------------- 28/08
# OK ALTERAR VALOR DA MENSALIDADE NA HORA DE INSERIR
# OK PERDOAR MENSALIDADE FUNCIONANDO ERRADO
# OK ESCREVER PERDOAR MENSALIDADE
# OK TESTAR - BACKUPS - IMPLEMENTAR <---------
# OK MENSALIDADE MESES PASSADOS - NO MOMENTO NÃO DÁ PRA RECEBER DE QUEM É CADASTRADO NO MÊS SEGUINTE
# - intervalos - marcar quantos dias até a pessoa retornar do intervalo
# - VALIDACAO de dados em todos os campos de entrada
# - implementar log de erros de acordo com
# https://stackoverflow.com/questions/3383865/how-to-log-error-to-file-and-not-fail-on-exception
# mudar a cor da linha na tabela quando um aluno estiver em pausa
# OK DESCONTO FAMILIA - VERIFICAR:
# OK - JANELA DE ADERIR PLANOS
# OK - JANELA MAIS INFORMACOES
# OK - RELATORIO DE VALORES RECEBIDOS
# OK - CONTÁBIL
# OK - JANELA COBRANCA
# OK - JANELA CADASTRO
# OK JANELA MAIS INFO - ALTERAR OPCAO DE TREINO DO ALUNO
# OK JANELA MAIS INFO - DESCONTO FAMÍLIA
# OK JANELA MAIS INFO - CORRIGIR PLANOS, MENSALIDADES COLOCAR QUAL MES QUE É A MENSALIDADE
# OK IMPLEMENTAR: ALUNO COM DESCONTO FAMILIA NAO PODE TER DESCONTO EM PLANOS
# OK FUNCAO PRA IMPRIMIR LISTA DE ALUNOS DEVEDORES NO RELATORIO DE NÃO PAGADORES
# OK CONSERTAR O RELATÓRIO DE NÃO PAGADORES MENSAL - INCLUI A FUNÇÃO PRA IMPRIMIR DEVEDORES - JANELA NAO FUNCIONA
# OK COMPRA NAO APARECE NA MENSALIDADE ATRASADA, MAS E CONTADO O VALOR
# OK IMPRESSAO RECIBO NA JANELA VENDER
# OK TERMINAR A CLASSE Aderir_planos
# OK IMPRESSAO NA JANELA PAGAMENTOS
# OK IMPRESSAO RECIBO NA JANELA RECEBER
# OK ALUNO INATIVO NAO CONTAR MENSALIDADE <--------------------- ACHO QUE TÁ OK
# OK IMPLEMENTAR DESCONTO BOM PAGADOR
# OK MULTA NA FUNCAO RECEBER MENSALIDADE NAO ESTA FUNCIONANDO - NAO TEM MAIS MULTA
# OK FUNCAO mensalidades_historico - fazer retornar o valor pago como moeda
# OK CONTABIL TÁ DANDO O VALOR RECEBIDO ERRADO
# OK INCLUIR NO CADASTRO DE ALUNOS UM SELETOR DE DATA, CASO CADASTRE NO MES ANTERIOR
# OK CORES DE ALUNOS EM ATRASO NA TABELA ESTÃO ERRADAS
# OK MENSALIDADE EM ATRASO ANTES DO VENCIMENTO
# MAIS OU MENOS OK - PODE MELHORAR DESCONTO FAMILIA!!!
# OK planos - planos de 3 meses pré pagos para vender
# OK mudar a cor da linha quando um aluno estiver com um plano
# OK TRANSFORMAR O PAGTO DE MENSALIDADES EM UMA TABELA
################################################################


# log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# formatter = logging.Formatter(log_format)
logging.basicConfig(filename='errorlog.txt', level=logging.DEBUG,
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

# sg.set_options(use_custom_titlebar=True)
locale.setlocale(locale.LC_ALL, '')

dbfile = os.path.join(os.getcwd(), 'db', 'sistema.db')
mdbfile = os.path.join(os.getcwd(), 'db', 'mensalidades.db')
imagem = os.path.join(os.getcwd(), 'recursos', 'logo.png')
barra = os.path.join(os.getcwd(), 'recursos', 'barra.png')
icones = [
    os.path.join(os.getcwd(), 'recursos', 'icones', 'banco.png'),
    os.path.join(os.getcwd(), 'recursos', 'icones', 'config.png'),
    os.path.join(os.getcwd(), 'recursos', 'icones', 'credito.png'),
    os.path.join(os.getcwd(), 'recursos', 'icones', 'erro.png'),
    os.path.join(os.getcwd(), 'recursos', 'icones', 'esporte.png'),
    os.path.join(os.getcwd(), 'recursos', 'icones', 'info.png'),
    os.path.join(os.getcwd(), 'recursos', 'icones', 'loja.png'),
    os.path.join(os.getcwd(), 'recursos', 'icones', 'pessoa.png'),
    os.path.join(os.getcwd(), 'recursos', 'icones', 'pix.png'),
]
imagem_peq = os.path.join(os.getcwd(), 'recursos', 'logo_small.png')
icone = os.path.join(os.getcwd(), 'recursos', 'logo_icon.ico')
ajustes = os.path.join(os.getcwd(), 'ajustes')
pdfviewer = os.path.join(os.getcwd(), 'recursos', 'SumatraPDF.exe')
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro',
         'Novembro', 'Dezembro']
dias = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab']

# ultimobkp = '10/06/2022'
ajuda = ''
regexTelefone = re.compile(r'^\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])[0-9]{3}(\-|\.)?[0-9]{4}$')  # OK
# ORIGINAL PARA TELEFONE: ^\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}$
regexCPF = re.compile(r'\d{3}\.\d{3}\.\d{3}\-\d{2}')
regexDinheiro = re.compile(r'^(\d{1,}\,\d{2}?)$')  # OK
regexEmail = re.compile(r'^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$')  # OK
regexDia = re.compile(r'\b[0-3]{0,1}[0-9]{1}\b')  # OK
regexDesconto = re.compile(r'\d\.\d{1,2}')
regexData = re.compile(r'\d{2}/\d{2}/\d{4}')
# arq_recibo = 'recibo.pdf'
# arq_relatorio = 'relatorio.pdf'

# REABILITAR A LINHA ABAIXO PARA O TEMA DE USUARIO
sg.theme(sg.user_settings_get_entry('-tema-'))
# sg.theme('Gray Gray Gray')
calendar.setfirstweekday(calendar.SUNDAY)


# sg.show_debugger_popout_window()

# INICIO FUNCAO RECRIA BANCO DE DADOS


def novobanco():
    try:
        shutil.copyfile(dbfile, dbfile + '.bkp')
    except OSError:
        # print('erro')
        sg.popup('Erro')
    if os.path.exists(dbfile):
        os.remove(dbfile)
    conn = sqlite3.connect(dbfile)
    conn.close()

    conn = sqlite3.connect(dbfile)
    # definindo um cursor
    cursor = conn.cursor()

    # criando a tabela (schema)
    cursor.execute("""
    CREATE TABLE "Alunos" (
    "al_index"	INTEGER,
    "al_nome"	TEXT,
    "al_endereco"	TEXT,
    "al_telefone01"	TEXT,
    "al_cpf"	TEXT,
    "al_email"	TEXT,
    "al_dt_matricula"	TEXT,
    "al_dt_vencto"	TEXT,
    "al_valmens"	TEXT,
    "al_ultimopagto"	TEXT,
    "al_ativo"	TEXT,
    PRIMARY KEY("al_index")
    );
    """)

    conn.close()

    conn = sqlite3.connect(dbfile)
    # definindo um cursor
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE "Financeiro" (
    "fi_nome"	INTEGER,
    "fi_data_pgto"	TEXT,
    "fi_atraso"	TEXT,
    "fi_valor_rec"	TEXT,
    "fi_recebido"	TEXT,
    FOREIGN KEY("fi_nome") REFERENCES "Alunos"("al_index")
    );
    """)

    conn.close()


# FINAL FUNCAO RECRIA BANCO DE DADOS

# FUNCAO VALIDA CPF

def valida_cpf(cpf: str) -> bool:
    """ Efetua a validação do CPF, tanto formatação quando dígito verificadores.
    Retirada de: https://pt.stackoverflow.com/questions/64608/
    como-validar-e-calcular-o-d%C3%ADgito-de-controle-de-um-cpf

    Parâmetros:
        cpf (str): CPF a ser validado

    Retorno:
        bool:
            - Falso, quando o CPF não possuir o formato 999.999.999-99;
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.

    Exemplos:

   # >>> valida_cpf('529.982.247-25')
    True
   # >>> valida_cpf('52998224725')
    False
   # >>> valida_cpf('111.111.111-11')
    False
    """

    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True


# FINAL FUNCAO VALIDA CPF

# verifica se é a primeira execução do programa no dia atual. se for, exibe splashscreen e tela de porcentagem.
def firstrun():
    # sg.user_settings_set_entry('-datalastrun-', datetime.strftime(date.today() + relativedelta(days=-1), '%Y-%m-%d'))
    tmp = sg.user_settings_get_entry('-datalastrun-', datetime.strftime(date.today(), '%Y-%m-%d'))
    tmpdata = date.fromisoformat(tmp)
    sg.user_settings_set_entry('-datalastrun-', datetime.strftime(date.today(), '%Y-%m-%d'))
    if tmpdata < date.today():
        return True
    else:
        return False


# FUNCAO VERIFICA SE TABELA EXISTE
def tableexists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT * FROM sqlite_master WHERE type = 'table' AND name = '{0}'
        """.format(tablename))  # .replace('\'', '\'\'')
    # SELECT * FROM sqlite_master WHERE type = 'table' AND name = 'the_table_name'
    # print(tablename)
    # print('dbcur.fetchone()[1] ', dbcur.fetchone())
    # print(dbcur.fetchone()[2])
    myvar = dbcur.fetchall()
    # print(myvar)
    if not myvar:
        dbcur.close()
        return False
    dbcur.close()
    return True


# FUNCAO CRIA TABELA NO DB MENSALIDADES
def mensalidades_cria_tabela(index):
    nometabela = 'mens_' + str(index)
    conexao = sqlite3.connect(mdbfile)
    comando = ('create table if not exists ' + nometabela + '(me_index INTEGER PRIMARY KEY, me_mesano TEXT, '
                                                            'me_diaven TEXT, me_valor TEXT, me_datapgto '
                                                            'TEXT, me_vlrmulta TEXT, me_vlrextras TEXT, me_vlrpago '
                                                            'TEXT, '
                                                            'me_pg INTEGER, me_atraso TEXT);')
    if not tableexists(conexao, nometabela):
        c = conexao.cursor()
        c.execute(comando)
    conexao.close()


def mensalidades_insere(index, mesano, diaven, valor, datapgto, vlrmulta, vlrextras, vlrpago, pg, atraso):
    """
    Insere dados na tabela mensalidade
    :param index:
    :param mesano:
    :param diaven:
    :param valor:
    :param datapgto:
    :param vlrmulta:
    :param vlrextras:
    :param vlrpago:
    :param pg:
    :param atraso:
    :return: 0 se não existir e for criado, 1 se existir e atualizado, 2 se existir e já pago
    """

    inserido = False
    inseredtultpgto = False
    dados = [mesano, diaven, valor, datapgto, vlrmulta, vlrextras, vlrpago, pg, atraso]
    conexao = sqlite3.connect(mdbfile)
    resultado = 0
    c = conexao.cursor()
    nometabela = 'mens_' + str(index)
    # primeiro, checa se o registro já existe
    comando = 'SELECT * FROM ' + nometabela
    c.execute(comando)
    cdados = c.fetchall()
    print('cdados(select da tabela): ', cdados)
    if cdados:
        # se existe, checa se já foi pago
        for idx, x in enumerate(cdados):
            if x[1] == mesano and x[8] != 1:
                # se a data da mensalidade for igual a data entrada na funcao, e
                # se a coluna me_pg for != 1 (ou seja não pago)
                dadosupdt = [mesano, diaven, valor, datapgto, vlrmulta, vlrextras, vlrpago, pg, atraso, x[0]]
                comando = 'UPDATE ' + nometabela + ' SET me_mesano = ?,' \
                                                   ' me_diaven = ?,me_valor = ?, me_datapgto = ?, me_vlrmulta = ?,' \
                                                   ' me_vlrextras = ?, me_vlrpago = ?, me_pg = ?, me_atraso = ?' \
                                                   ' WHERE me_index = ?'
                c.execute(comando, dadosupdt)
                resultado = 1
                inseredtultpgto = True
                inserido = True
            if x[1] == mesano and x[8] == 1:
                resultado = 2
                inserido = True
        if not inserido:
            comando = 'INSERT INTO ' + nometabela + '(me_mesano,me_diaven,me_valor,me_datapgto' \
                                                    ',me_vlrmulta,me_vlrextras,' \
                                                    'me_vlrpago,me_pg,me_atraso) VALUES (?,?,?,?,?,?,?,?,?)'
            c.execute(comando, dados)
            resultado = 0
            inseredtultpgto = False
    else:
        comando = 'INSERT INTO ' + nometabela + '(me_mesano,me_diaven,me_valor,me_datapgto' \
                                                ',me_vlrmulta,me_vlrextras,' \
                                                'me_vlrpago,me_pg,me_atraso) VALUES (?,?,?,?,?,?,?,?,?)'
        c.execute(comando, dados)
        resultado = 0
        inseredtultpgto = True
    conexao.commit()
    conexao.close()
    if inseredtultpgto:
        # insere a data do ultimo pagamento na tabela alunos
        secinsert = [datapgto, index]
        conexao = sqlite3.connect(dbfile)
        c = conexao.cursor()
        c.execute('UPDATE Alunos SET al_ultimopagto = ? WHERE al_index = ?', secinsert)
        conexao.commit()
        conexao.close()
    return resultado


def mensalidades_insere_plano(alunoindex, mesano, diaven, valor, datapgto, vlrmulta, vlrextras, vlrpago, pg, atraso,
                              plindex, pldescricao, plinicio, plfim):
    """
    Insere os dados do plano na tabela alunos, e cria os dados de mensalidade na tabela mensalidades,
    registrando a mensalidade como paga. Esta função cria SOMENTE UMA VEZ a mensalidade, portanto deve
    ser executada quantas vezes for necessário, incrementando a data(mesano) de acordo com os meses do
    plano adquirido.
    :param alunoindex: Índice do aluno
    :param mesano: mês e ano do primeiro pagamento
    :param diaven: dia de vencimento
    :param valor: valor com desconto
    :param datapgto: data do primeiro pagamento
    :param vlrmulta: valor do desconto
    :param vlrextras:
    :param vlrpago:
    :param pg:
    :param atraso:
    :param plindex:
    :param pldescricao:
    :param plinicio:
    :param plfim:
    :return:
    """
    inseredtultpgto = False
    dados = [mesano, diaven, valor, datapgto, vlrmulta, vlrextras, vlrpago, pg, atraso]
    conexao = sqlite3.connect(mdbfile)
    resultado = 0
    c = conexao.cursor()
    nometabela = 'mens_' + str(alunoindex)
    # primeiro, checa se o registro já existe
    comando = 'SELECT * FROM ' + nometabela + ' WHERE me_mesano = ?'
    c.execute(comando, (mesano,))
    cdados = c.fetchone()
    #  TODO: verificar se esta funcao vai inserir a mensalidade não paga do mes atual
    if cdados:
        # se existe, checa se já foi pago
        if cdados[8] != 1:
            # se a coluna me_pg for != 1 (ou seja não pago)
            dadosupdt = [mesano, diaven, valor, datapgto, vlrmulta, vlrextras, vlrpago, pg, atraso, cdados[0]]
            comando = 'UPDATE ' + nometabela + ' SET me_mesano = ?,' \
                                               ' me_diaven = ?,me_valor = ?, me_datapgto = ?, me_vlrmulta = ?,' \
                                               ' me_vlrextras = ?, me_vlrpago = ?, me_pg = ?, me_atraso = ?' \
                                               ' WHERE me_index = ?'
            c.execute(comando, dadosupdt)
            resultado = 1
            inseredtultpgto = True
        if cdados[8] == 1:
            # se a mensalidade já foi paga
            resultado = 2
    else:
        # se não existe a informação da mensalidade
        comando = 'INSERT INTO ' + nometabela + '(me_mesano,me_diaven,me_valor,me_datapgto' \
                                                ',me_vlrmulta,me_vlrextras,' \
                                                'me_vlrpago,me_pg,me_atraso) VALUES (?,?,?,?,?,?,?,?,?)'
        c.execute(comando, dados)
        resultado = 0
        inseredtultpgto = True
    conexao.commit()
    conexao.close()
    if inseredtultpgto:
        # insere a data do ultimo pagamento na tabela alunos
        secinsert = [datapgto, plindex, pldescricao, plinicio, plfim, alunoindex]
        conexao = sqlite3.connect(dbfile)
        c = conexao.cursor()
        c.execute('UPDATE Alunos SET al_ultimopagto = ?, al_planoindex = ?, al_plano = ?, '
                  'al_pl_inicio = ?, al_pl_fim = ? WHERE al_index = ?', secinsert)
        conexao.commit()
        conexao.close()
    return resultado


def mensalidades_atraso(index):
    # RETORNA UMA LISTA DATA DAS MENSALIDADES EM ATRASO.
    conexao = sqlite3.connect(mdbfile)
    mensatraso = []
    c = conexao.cursor()
    nometabela = 'mens_' + str(index)
    comando = 'SELECT * FROM ' + nometabela
    c.execute(comando)
    cdados = c.fetchall()
    # print(cdados)
    if cdados:
        for idx, x in enumerate(cdados):
            if x[8] != 1:
                if x[1]:
                    if x[2]:
                        tmpdia = int(x[2])
                        tmpdata = datetime.strptime((str(tmpdia) + '/' + x[1]), '%d/%m/%Y')
                        tmpdata = tmpdata + relativedelta(days=+10)
                        if tmpdata < datetime.now():
                            mensatraso.append(x[1])
    # print('Index: ', index, ' mensatraso: ', mensatraso)
    conexao.close()
    return mensatraso


def mensalidades_a_pagar(index):
    conexao = sqlite3.connect(mdbfile)
    mensalidades = []
    c = conexao.cursor()
    nometabela = 'mens_' + str(index)
    comando = 'SELECT * FROM ' + nometabela
    c.execute(comando)
    cdados = c.fetchall()
    # print(cdados)
    if cdados:
        for idx, x in enumerate(cdados):
            if x[8] != 1:
                if x[1]:
                    tmpdia = int(x[2])
                    tmpdata = datetime.strftime(
                        datetime.strptime((str(tmpdia) + '/' + x[1]), '%d/%m/%Y'), '%d/%m/%Y')
                    mensalidades.append([x[2], tmpdata, x[3]])
    # RETORNA dia do vencimento, data completa do vencimento, valor
    # print('Index: ', index, ' mensatraso: ', mensalidades)
    conexao.close()
    return mensalidades


# FUNCAO PUXA TODOS OS DADOS DO REGISTRO ATRASADO NA TABELA MENSALIDADES
def mensalidades_ler_atrasado(index, mesano):
    conexao = sqlite3.connect(mdbfile)
    c = conexao.cursor()
    # dados = [mesano]
    nometabela = 'mens_' + str(index)
    comando = 'SELECT * FROM ' + nometabela + ' WHERE me_mesano = ?'
    c.execute(comando, (mesano,))
    dados = c.fetchall()[0]
    conexao.close()
    return dados


# FUNCAO CRIA MENSALIDADE ATRASADA NAS TABELAS
def mensalidades_criar():
    """
    Cria as mensalidades dos alunos conforme os meses vão passando. As tabelas de mensalidades precisam
    ter as mensalidades à pagar inseridas antes que estas possam ser pagas, para que já exista
    o objeto na hora do pagamento. Esta função deve ser executada no início do programa.
    :return: None.
    """
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    dia = datetime.strftime(datetime.now(), '%d')
    # mesano = '"' + datetime.strftime(datetime.now(), '%m/%Y') + '"'
    mesano = datetime.strftime(datetime.now(), '%m/%Y')
    comando = 'SELECT al_index, al_dt_vencto, ' \
              'al_valmens from Alunos WHERE al_dt_vencto < ' + dia + ' AND al_ativo = "S"'
    # print(mesano)
    c.execute(comando)
    diasvencto = c.fetchall()
    # print(diasvencto)
    conexao.close()
    conexao = sqlite3.connect(mdbfile)
    c = conexao.cursor()
    if diasvencto:
        for idx, x in enumerate(diasvencto):
            nometabela = 'mens_' + str(x[0])
            # print(nometabela)
            # print(str(x[0]))
            valorstr = x[2].replace(',', '.')
            # nometabela = 'mens_1'
            # dados = [x[1], x[2], mesano]
            # dados = [mesano]
            comando = 'INSERT INTO ' + nometabela + \
                      ' (me_mesano,me_diaven,me_valor,me_pg) SELECT "' + mesano + \
                      '", "' + x[1] + '", "' + valorstr + '", "0" WHERE NOT EXISTS ' \
                                                          '(SELECT 2 FROM ' + nometabela + ' WHERE me_mesano = "' + mesano + '")'
            # comando = 'UPDATE ' + nometabela + ' SET me_diaven= ?,me_valor = ? WHERE me_mesano = ?'
            # comando = 'DELETE FROM ' + nometabela + ' WHERE me_mesano = ?'
            # print(comando)
            # comando = 'SELECT * FROM ' + nometabela + ' WHERE me_mesano = ?'
            c.execute(comando)
        conexao.commit()
    conexao.close()


# FUNCAO LISTA MENSALIDADES ANTIGAS
def mensalidades_lista(index):
    """
    DEPRECATED: esta função não é mais utilizada. Ela deve ser eventualmente excluída.
    :param index:
    :return:
    """
    conexao = sqlite3.connect(mdbfile)
    c = conexao.cursor()
    nometabela = 'mens_' + str(index)
    comando = 'SELECT me_index, me_datapagto, me_atraso, me_valor, me_vlrpago FROM ' + nometabela
    c.execute(comando)
    dados = c.fetchall()
    conexao.close()
    return dados


#  funcao que busca a ultima mensalidade paga
def mensalidades_ultima_paga(index):
    """
    Função utilizada no momento em que o aluno vai aderir a um plano. Retorna 0 se não houver mensalidade
    paga, ou uma lista de mesano da última mensalidade paga.
    :param index:
    :return:
    """
    # Retorna 0 se não houver mensalidade paga, ou mesano da ultima paga
    nometabela = 'mens_' + str(index)
    conexao = sqlite3.connect(mdbfile)
    c = conexao.cursor()
    comando = 'SELECT me_mesano FROM ' + nometabela + ' WHERE me_pg = 1'
    # print(comando)
    c.execute(comando)
    mensalidades = c.fetchall()
    # print('mensalidades: ', mensalidades)
    conexao.close()
    if mensalidades:
        mensalidades_sorted = sorted(mensalidades)
        resultado = mensalidades_sorted[len(mensalidades_sorted) - 1]
    else:
        resultado = 0
    # for idx, x in enumerate(mensalidades):
    #     if x[0] == 'S':
    print('resultado: ', resultado)
    return resultado


# FUNCAO RELATORIO DE MENSALIDADES RECEBIDAS
def mensalidades_relatorio(mesano):
    # RETORNA data de pagamento, nome do aluno, atraso e valor pago.
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT al_index, al_nome FROM Alunos')
    indicenome = c.fetchall()
    conexao.close()
    conexao = sqlite3.connect(mdbfile)
    c = conexao.cursor()
    dados = []
    mesano = ('%' + mesano + '%')
    for idx, x in enumerate(indicenome):
        # temp = []
        nometabela = 'mens_' + str(x[0])
        comando = 'SELECT me_datapgto, me_atraso, me_vlrpago, me_pg FROM ' + nometabela + ' WHERE me_mesano LIKE ?'
        c.execute(comando, (mesano,))
        temp = c.fetchone()
        if temp is not None:
            if temp[3] == 1 and not None:
                temp2 = [temp[0], x[1], temp[1], temp[2]]
                dados.append(temp2)
    # dadoslinha = []
    dadoscolunas = []
    for idx, x in enumerate(dados):
        dadoslinha = []
        for idi, i in enumerate(x):
            i = xstr(i)
            dadoslinha.append(i)
            # print(dadoslinha)
        dadoscolunas.append(dadoslinha)
    conexao.close()
    # RETORNA data de pagamento, nome do aluno, atraso e valor pago.
    return dadoscolunas


def mensalidades_porcentagem(mesano):
    """
    Entrega dados para a criação do gráfico de pagamento de mensalidades.
    :param mesano: string (mes/ano)
    :return: f_pago (float), f_npago (float), qtd_alunos (int)
    """
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT al_index FROM Alunos')
    alunos = c.fetchall()
    # qtd_alunos = len(alunos)
    # print('Contagem de linhas: ', qtd_alunos)
    conexao.close()
    conexao = sqlite3.connect(mdbfile)
    c = conexao.cursor()
    temp = []
    naopago = 0
    pago = 0
    arraytmp = []
    for idx, x in enumerate(alunos):
        nometabela = 'mens_' + str(x[0])
        comando = 'SELECT me_pg FROM ' + nometabela + ' WHERE me_mesano LIKE ?'
        c.execute(comando, (mesano,))
        temp = c.fetchone()
        print('temp', temp)
        arraytmp.append(temp)
    # print('arraytmp: ', arraytmp[0][0])
    for idx, x in enumerate(arraytmp):
        if x is not None:
            print('x: ', x)
            # final_x = x.translate({ord(c): None for c in "(,)"})
            if x[0] == 0:
                naopago = naopago + 1
            else:
                pago = pago + 1
    qtd_alunos = naopago + pago
    f_pago, f_npago = 0.0, 0.0
    if qtd_alunos != 0:
        print('Pago: ', pago)
        print('Nao pago: ', naopago)
        if pago != 0:
            f_pago = (pago / qtd_alunos) * 100
        if naopago != 0:
            f_npago = (naopago / qtd_alunos) * 100
    # print('Pagos: ', f_pago)
    # print('Não pagos: ', f_npago)
    return f_pago, f_npago, qtd_alunos


# FUNCAO QUE OCUPA O LUGAR DE BUSCA_DADOS_FINANCEIROS
def mensalidades_historico(indice):
    """
    Cria uma lista com as informações das mensalidades pagas
    :param indice: índice do aluno
    :return: indice, mesano, data de pagto, valor pago da mensalidade.
    """
    # RETORNA indice, mesano da mens., data de pagamento, valor pago
    nometabela = 'mens_' + str(indice)
    conexao = sqlite3.connect(mdbfile)
    c = conexao.cursor()
    # comando = 'SELECT me_index, me_mesano, me_datapgto, me_vlrpago FROM ' + nometabela + ' WHERE me_pg = 1'
    comando = 'SELECT me_index, me_mesano, me_datapgto, me_vlrpago FROM ' + nometabela
    c.execute(comando)
    mensalidades = c.fetchall()
    mensalidades_moeda = []
    for idx, x in enumerate(mensalidades):
        if x[3]:
            tmp = locale.currency(float(x[3]))
            mensalidades_moeda.append([x[0], x[1], x[2], tmp])
        else:
            mensalidades_moeda.append([x[0], x[1], '--', '--'])
    dadoscolunas = []
    for idx, x in enumerate(mensalidades_moeda):
        dadoslinha = []
        for idi, i in enumerate(x):
            i = xstr(i)
            dadoslinha.append(i)
            # print(dadoslinha)
        dadoscolunas.append(dadoslinha)
    conexao.close()
    # RETORNA indice, mesano da mens., data de pagamento, valor pago
    dadossort = sort_table(dadoscolunas, (1, 0))
    return dadossort


# FUNCAO LE A TABELA OPCAO
def opcao_ler():
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT * FROM Opcao')
    resultado = c.fetchall()
    conexao.close()
    return resultado


# FUNCAO LE A TABELA OPCAO
def opcao_apagar(indice):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('DELETE FROM Opcao WHERE op_index = ?', (indice,))
    conexao.commit()
    conexao.close()


# FUNCAO LE APENAS A DESCRICAO NA TABELA OPCAO
def opcao_ler_desc():
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT op_desc FROM Opcao')
    resultado = c.fetchall()
    conexao.close()
    resultado2 = []
    # print(list(zip(*resultado))[0])
    # print(type(resultado))
    resultado2 = list(zip(*resultado))[0]
    return resultado2


# FUNCAO ATUALIZA A OPCAO DO ALUNO NA TABELA ALUNOS

def opcao_atualiza(indicealuno, indiceopcao, descricao, dias2):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    # c.execute('SELECT al_pl_fim FROM Alunos WHERE al_index', (index,))
    # tmpresult = c.fetchone()
    dados = [indiceopcao, descricao, dias2, indicealuno]
    c.execute(
        'UPDATE Alunos SET al_op_index = ?, al_op_desc = ?, al_op_dias = ? WHERE '
        'al_index = ?',
        dados)
    conexao.commit()
    conexao.close()


# FUNCAO RETORNA OS DADOS DA TABELA OPCAO PELA DESCRICAO
def opcao_buscar_desc(desc):
    # retorna zero se não houver dados
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT * FROM Opcao WHERE op_desc = ?', (desc,))
    resultado = c.fetchone()
    conexao.close()
    if not resultado:
        resultado = 0
    return resultado


# Função que grava as alterações na opção ou uma nova opção
# Update/Insere descrição, dias e valor
def opcao_escreve(index, descricao, dias2, valor):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT * FROM Opcao WHERE op_index = ?', (index,))
    resultado = c.fetchone()
    dados = [descricao, dias2, valor, index]
    if resultado:
        comando = 'UPDATE Opcao SET op_desc = ?, op_diassemana = ?, op_valor = ? WHERE op_index = ?'
        c.execute(comando, dados)
    else:
        dados = [descricao, dias2, valor]
        comando = 'INSERT INTO Opcao(op_desc, op_diassemana, op_valor) VALUES (?, ?, ?)'
        c.execute(comando, dados)
    conexao.commit()
    conexao.close()


# FUNCAO LE A TABELA PLANOS
def planos_ler():
    # retorna indice do plano, descrição, período (em meses), valor em porcentagem
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT * FROM Planos')
    resultado = c.fetchall()
    conexao.close()
    return resultado


# FUNCAO BUSCA OS DADOS DO PLANO INSCRITO DO ALUNO
def planos_busca(index):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT al_planoindex, al_plano, al_pl_inicio, al_pl_fim FROM Alunos WHERE al_index = ?', (index,))
    resultado = c.fetchone()
    conexao.close()
    return resultado


# ESCREVE OS DADOS DO PLANO DO ALUNO
def planos_escreve(index, planoindex, plano, inicio, fim, duracao, vlrmensal):
    """
    Entra com os dados do plano na tabela alunos e na tabela mensalidade
    :param index:
    :param planoindex:
    :param plano:
    :param inicio: data no formato 00/00/0000
    :param fim: data no formato 00/00/0000
    :param duracao:
    :param vlrmensal:
    :return:
    """
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    # c.execute('SELECT al_pl_fim FROM Alunos WHERE al_index', (index,))
    # tmpresult = c.fetchone()
    dados = [planoindex, plano, inicio, inicio, fim, index]
    c.execute(
        'UPDATE Alunos SET al_planoindex = ?, al_plano = ?, al_pl_inicio = ?, al_ultimopagto = ?, al_pl_fim = ? WHERE '
        'al_index = ?',
        dados)
    conexao.commit()
    conexao.close()
    dadosmens = []
    # ###################################################################################################
    dia = inicio[0:2]
    # ano = inicio[6:]
    inicio_date = datetime.strptime(inicio, '%d/%m/%Y')
    # print(inicio[3:5])
    # mesint = int(inicio[3:5])
    x = 0
    mesano = []
    while x < duracao:
        if x > 0:
            inicio_date = inicio_date + relativedelta(months=+1)
        else:
            pass
        messtr = inicio_date.strftime('%m/%Y')
        mesano.append(messtr)
        x = x + 1
    conexao = sqlite3.connect(mdbfile)
    c = conexao.cursor()
    nometabela = 'mens_' + str(index)
    print(mesano)
    for idx, x in enumerate(mesano):
        dados = [x, dia, inicio, vlrmensal, 1]
        comando = 'INSERT INTO ' + nometabela + '(me_mesano, me_diaven, me_datapgto, me_vlrpago, me_pg) VALUES (?,?,' \
                                                '?,?,?) '
        c.execute(comando, dados)
        conexao.commit()
    conexao.close()


def planos_grava(index, descricao, meses2, valor):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT * FROM Planos WHERE pl_index = ?', (index,))
    resultado = c.fetchone()
    dados = [descricao, meses2, valor, index]
    if resultado:
        comando = 'UPDATE Planos SET pl_desc = ?, pl_periodo = ?, pl_valor = ? WHERE pl_index = ?'
        c.execute(comando, dados)
    else:
        dados = [descricao, meses2, valor]
        comando = 'INSERT INTO Planos(pl_desc, pl_periodo, pl_valor) VALUES (?, ?, ?)'
        c.execute(comando, dados)
    conexao.commit()
    conexao.close()


def planos_apagar(indice):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('DELETE FROM Planos WHERE pl_index = ?', (indice,))
    conexao.commit()
    conexao.close()


# FUNCAO CHECA SE O PLANO ESTA NO FINAL
def planos_acabando(index):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT al_pl_fim FROM Alunos WHERE al_index = ?', (index,))
    resultado = c.fetchone()[0]
    # print(resultado)
    conexao.close()
    return resultado


def aluno_inativo(index):
    """
    Checa se o aluno está inativo
    :param index:
    :return: status do aluno
    """
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT al_ativo FROM Alunos WHERE al_index = ?', (index,))
    resultado = c.fetchone()[0]
    # print(resultado)
    conexao.close()
    return resultado


# FUNCAO PEGA O al_index DO ULTIMO REGISTRO DA TABELA
def alunos_ultimo():
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT max(al_index) FROM Alunos')
    dados = c.fetchone()[0]
    #    for linha in c.fetchall():
    #        print(linha)
    conexao.close()
    return dados


#  RETORNA O NOME E A DATA DE VENCIMENTO DE TODOS OS ALUNOS ATIVOS
def alunos_nomeven():
    temp_tabela = ler_todos_dados_ativos()
    resultado = []
    for idx, x in enumerate(temp_tabela):
        resultado.append([x[0], x[1], x[7]])
        # INDICE, NOME, DT VENCTO
    # print(resultado)
    return resultado


# INICIO FUNCAO MES ATUAL
def mesatual():
    res = ''
    mesat = datetime.now()
    m = mesat.strftime('%m')
    if m == '01':
        res = meses[0]
    elif m == '02':
        res = meses[1]
    elif m == '03':
        res = meses[2]
    elif m == '04':
        res = meses[3]
    elif m == '05':
        res = meses[4]
    elif m == '06':
        res = meses[5]
    elif m == '07':
        res = meses[6]
    elif m == '08':
        res = meses[7]
    elif m == '09':
        res = meses[8]
    elif m == '10':
        res = meses[9]
    elif m == '11':
        res = meses[10]
    elif m == '12':
        res = meses[11]
    return res


# FINAL FUNCAO MES ATUAL

# # INICIO FUNCAO GERA RECIBO
# def gera_recibo_pdf(nome, valorpago, datapgto, datavencto, atraso, usuario):
#     rpdf = FPDF('P', 'cm', 'A4')
#     rpdf.add_page()
#     rpdf.add_font('Calibri', 'I', 'Calibrii.ttf', uni=True)
#     rpdf.add_font('Calibri', 'B', 'Calibrib.ttf', uni=True)
#     rpdf.add_font('Calibri', '', 'Calibri.ttf', uni=True)
#     rpdf.set_font('Calibri', 'B', 14)
#     rpdf.image(imagem_peq, 16.6, 1.6)
#     rpdf.rect(1, 1, 19, 8.8, 'D')
#     rpdf.cell(0, 0.6, '', 0, 2, 'C')
#     rpdf.cell(0, 0.6, 'RECIBO DE PAGAMENTO DE MENSALIDADE', 0, 2, 'C')
#     rpdf.cell(0, 0.6, 'Lótus Condicionamento Dinâmico Integrado', 0, 2, 'C')
#     rpdf.cell(0, 0.6, 'Andréia de Cássia Gonçalves (CREF 020951-G/MG)', 0, 2, 'C')
#     rpdf.set_font('Calibri', 'I', 14)
#     rpdf.cell(0, 0.6, 'Rua Coronel Paiva, 12  Centro  Ouro Fino MG', 0, 2, 'C')
#     rpdf.line(1, 4.5, 20, 4.5)
#     rpdf.set_font('Calibri', 'B', 14)
#     rpdf.cell(0.5, 1, '', 0, 1)
#     rpdf.cell(0.5, 1, '')
#     rpdf.cell(3.5, 1, 'Nome do aluno: ')
#     rpdf.set_font('Calibri', '', 14)
#     rpdf.cell(0, 1, nome, 0, 1)
#     rpdf.set_font('Calibri', 'B', 14)
#     rpdf.cell(0.5, 1, '')
#     rpdf.cell(4.6, 1, 'Valor do pagamento: ')
#     rpdf.set_font('Calibri', '', 14)
#     rpdf.cell(2.5, 1, valorpago)
#     rpdf.set_font('Calibri', 'B', 14)
#     rpdf.cell(0.5, 1, '')
#     rpdf.cell(4.5, 1, 'Data do pagamento: ')
#     rpdf.set_font('Calibri', '', 14)
#     rpdf.cell(1, 1, datapgto, 0, 1)
#     rpdf.set_font('Calibri', 'B', 14)
#     rpdf.cell(0.5, 1, '')
#     rpdf.cell(4.6, 1, 'Dia do vencimento: ')
#     rpdf.set_font('Calibri', '', 14)
#     rpdf.cell(3, 1, datavencto)
#     rpdf.set_font('Calibri', 'B', 14)
#     rpdf.cell(1.7, 1, 'Atraso: ')
#     rpdf.set_font('Calibri', '', 14)
#     rpdf.cell(1, 1, atraso + ' dias', 0, 1)
#     rpdf.cell(0.5, 1, '')
#     rpdf.set_font('Calibri', 'B', 14)
#     rpdf.cell(3.2, 1, 'Recebido por: ')
#     rpdf.set_font('Calibri', '', 14)
#     rpdf.cell(2.5, 1, usuario)
#     # rpdf.cell(19, 10, 'Hello World!', 1)
#     # rpdf.cell(40, 10, 'Hello World!', 1)
#     # rpdf.cell(60, 10, 'Powered by FPDF.', 0, 1, 'C')
#     # rpdf.output(arq_recibo, 'F')
#     rpdf.output(pdfgen.arq_recibo)


# FINAL FUNCAO GERA RECIBO


# INICIO FUNCAO APAGA REGISTROS
def apaga_registro(index):
    # todo alterar esta funcao
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    # c.execute('DELETE FROM Financeiro WHERE fi_nome = ?', (index,))
    # c.execute('DELETE FROM Alunos WHERE al_index = ?', (index,))
    ativo = 'N'
    c.execute('UPDATE Alunos SET al_ativo = ? WHERE pl_index = ?', (ativo, index))
    conexao.commit()
    conexao.close()


# FINAL FUNCAO APAGA REGISTROS

# INICIO FUNCAO LEITURA DOS DADOS
def ler_todos_dados():
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute("""
                SELECT al_index,al_nome,al_endereco,al_telefone01,al_cpf,
                al_email,al_dt_matricula,al_dt_vencto,al_valmens,
                al_ultimopagto,al_ativo,al_planoindex,al_plano,al_pl_inicio,al_pl_fim,al_pl_renova,al_pausa,
                al_op_index,al_op_desc,al_op_dias,al_desc FROM Alunos;
            """)
    dados = c.fetchall()
    conexao.close()
    dadoscolunas = []
    for idx, x in enumerate(dados):
        dadoslinha = []
        for idi, i in enumerate(x):
            i = xstr(i)
            dadoslinha.append(i)
        dadoscolunas.append(dadoslinha)
    return dadoscolunas


# FINAL FUNCAO LEITURA DOS DADOS

def xstr(s):
    if s is None:
        return ''
    else:
        return s


# INICIO FUNCAO LEITURA DOS DADOS ATIVOS
def ler_todos_dados_ativos():
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute("""
                SELECT al_index,al_nome,al_endereco,al_telefone01,al_cpf,
                al_email,al_dt_matricula,al_dt_vencto,al_valmens,
                al_ultimopagto,al_ativo,al_planoindex,al_plano,al_pl_inicio,al_pl_fim,al_pl_renova,al_pausa,
                al_op_index,al_op_desc,al_op_dias,al_desc 
                FROM Alunos WHERE al_ativo = 'S';
            """)
    dados = c.fetchall()
    dadoslinha = []
    dadoscolunas = []
    for idx, x in enumerate(dados):
        dadoslinha = []
        for idi, i in enumerate(x):
            i = xstr(i)
            dadoslinha.append(i)
        dadoscolunas.append(dadoslinha)
    conexao.close()
    return dadoscolunas


# FINAL FUNCAO LEITURA DOS DADOS ATIVOS

# FUNCAO - LOCALIZAR ALUNO
def buscar_por_nome(nome, ret_ativos):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    # print(nome)
    nome = ('%' + nome + '%')
    # print(nome)
    if ret_ativos:
        c.execute("""
            SELECT al_index,al_nome,al_endereco,al_telefone01,al_cpf,
                al_email,al_dt_matricula,al_dt_vencto,al_valmens,
                al_ultimopagto,al_ativo,al_planoindex,al_plano,al_pl_inicio,al_pl_fim,al_pl_renova,al_pausa,
                al_op_index,al_op_desc,al_op_dias,al_desc FROM Alunos WHERE al_nome like ? 
                AND al_ativo = "S" """, (nome,))
    if not ret_ativos:
        c.execute("""
            SELECT al_index,al_nome,al_endereco,al_telefone01,al_cpf,
                al_email,al_dt_matricula,al_dt_vencto,al_valmens,
                al_ultimopagto,al_ativo,al_planoindex,al_plano,al_pl_inicio,al_pl_fim,al_pl_renova,al_pausa,
                al_op_index,al_op_desc,al_op_dias,al_desc
             FROM Alunos WHERE al_nome like ? """, (nome,))
    dados = c.fetchall()
    # print(resultado)
    conexao.close()
    dadoscolunas = []
    for idx, x in enumerate(dados):
        dadoslinha = []
        for idi, i in enumerate(x):
            i = xstr(i)
            dadoslinha.append(i)
            # print(dadoslinha)
        dadoscolunas.append(dadoslinha)
    return dadoscolunas


# FIM FUNCAO - LOCALIZAR ALUNO


# FUNCAO - CADASTRO DE ALUNO
def cadastrar_aluno(nome, endereco, tel1, cpf, email, mat, venc, valmens, ativo, opindex, opdesc, opdias, desc):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    dadosinsert = [nome, endereco, tel1, cpf, email, mat, venc, valmens, ativo, opindex, opdesc, opdias, desc]
    c.execute(
        "INSERT INTO Alunos(al_nome,al_endereco,al_telefone01,al_cpf,al_email,al_dt_matricula,al_dt_vencto,"
        "al_valmens,al_ativo,al_op_index,al_op_desc,al_op_dias,al_desc) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        dadosinsert)
    conexao.commit()
    conexao.close()


# FIM FUNCAO - CADASTRO DE ALUNO

# FUNCAO ADICIONA VENDA

def venda_adiciona(relalunos, data, desc, valor, cobra, formapgt, pg):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    dadosinsert = [relalunos, data, desc, valor, cobra, formapgt, pg]
    c.execute(
        "INSERT INTO Vendas(ve_relalunos,"
        " ve_data, ve_desc, ve_valor, ve_cobra, ve_formapgt, ve_pg) VALUES (?,?,?,?,?,?,?)",
        dadosinsert)
    conexao.commit()
    conexao.close()


# FUNCAO LE VENDA

def venda_busca(indicealuno):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    iterable = [indicealuno]
    c.execute("""
                    SELECT ve_index,ve_data,ve_desc,ve_valor,
                    ve_cobra,ve_formapgt,ve_pg FROM Vendas WHERE ve_relalunos = ?;
                """, iterable)
    dados = c.fetchall()
    conexao.close()
    return dados


# FUNCAO RECEBE VENDA

def venda_recebe(indice, data):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    data = ('%' + data + '%')
    vcobraset = 'NAO'
    senaopago = 'NAO'
    vpg = 'SIM'
    dados = [vcobraset, vpg, indice, data, senaopago]
    c.execute(
        "UPDATE Vendas SET ve_cobra = ?, ve_pg = ? WHERE ve_relalunos = ? AND ve_data like ? AND ve_pg = ?", dados)
    conexao.commit()
    conexao.close()


# FUNCAO ALTERA CADASTRO DE ALUNO
def alterar_aluno(nome, endereco, tel1, cpf, email, mat, venc, valmens, ativo, desc, indice):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    dadosinsert = [nome, endereco, tel1, cpf, email, mat, venc, valmens, ativo, desc, indice]
    c.execute(
        "UPDATE Alunos SET al_nome = ?, al_endereco = ?, al_telefone01 = ?, al_cpf = ?, al_email = ?, al_dt_matricula "
        "= ?, al_dt_vencto = ?, al_valmens = ?, al_ativo = ?, al_desc = ? WHERE al_index = ?",
        dadosinsert)
    conexao.commit()
    conexao.close()


# FIM FUNCAO ALTERA CADASTRO DE ALUNO

# FUNCAO LE ARQUIVO DE TEXTO
def abrir_texto(nomearquivo):
    f = open(os.path.join(os.getcwd(), 'ajuda', nomearquivo))
    texto = f.read()
    f.close()
    return texto


# FIM FUNCAO LE ARQUIVO DE TEXTO


# DEF BUSCA DADOS NA TABELA FINANCEIRO
def busca_dados_financeiros(indice):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    # c.execute('SELECT al_nome,al_endereco,al_telefone01,al_telefone02,al_email,al_dt_matricula,al_dt_vencto FROM
    # Alunos WHERE al_index = ?', (indice,))
    c.execute(
        'SELECT fi_nome,fi_data_pgto,fi_atraso,fi_valor_rec,fi_recebido FROM Financeiro fin JOIN Alunos al on '
        'fin.fi_nome = al.al_index WHERE al.al_index = ?',
        (indice,))
    resultado = c.fetchall()
    # print('tamanho resultado')
    # print(len(resultado))
    conexao.close()
    return resultado


# FIM DEF BUSCA DADOS NA TABELA FINANCEIRO

def mensalidade_busca(index):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    # c.execute('SELECT al_nome,al_endereco,al_telefone01,al_telefone02,al_email,al_dt_matricula,al_dt_vencto FROM
    # Alunos WHERE al_index = ?', (indice,))
    c.execute(
        'SELECT fi_data_pgto FROM Financeiro WHERE fi_nome = ?', (index,))
    resultado = c.fetchall()
    conexao.close()
    return resultado


# FUNCAO APAGA DADOS FINANCEIROS
def apaga_dados_financeiros(aluno, data):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('DELETE FROM Financeiro WHERE fi_nome = ? AND fi_data_pgto = ?', (aluno, data))
    # c.execute('SELECT fi_nome,fi_data_pgto,fi_atraso,fi_valor_rec,fi_recebido FROM Financeiro fin JOIN Alunos al on
    # fin.fi_nome = al.al_index WHERE al.al_index = ?', (indice,))
    conexao.commit()
    conexao.close()


# FINAL FUNCAO APAGA DADOS FINANCEIROS


# FUNCAO GERA RELATORIO FINANCEIRO MENSAL
def rel_fin_mensal(mesano):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()

    # c.execute('SELECT al_nome,al_endereco,al_telefone01,al_telefone02,al_email,al_dt_matricula,al_dt_vencto FROM
    # Alunos WHERE al_index = ?', (indice,))

    # c.execute('SELECT fi_data_pgto,fi_atraso,fi_valor_rec,fi_recebido FROM Financeiro fin JOIN Alunos al on
    # fin.fi_nome = al.al_index WHERE al.al_index = ?', (indice,))

    mesano = ('%' + mesano + '%')
    #    c.execute('SELECT fi_nome,* FROM Financeiro WHERE fi_data_pgto LIKE ?', (mesano,))
    c.execute(
        'SELECT * FROM Financeiro JOIN Alunos on Financeiro.fi_nome = Alunos.al_index WHERE fi_data_pgto LIKE ? AND '
        'Alunos.al_ativo = "S"',
        (mesano,))
    resultado = c.fetchall()
    # print(resultado)
    # FILTRANDO O RESULTADO:
    # print(resultado)
    i = 0
    res_filtrado = resultado
    while i < len(resultado):
        res_filtrado[i] = resultado[i][1], resultado[i][6], resultado[i][2], resultado[i][4], resultado[i][3]
        # fi_data_pgto, al_nome, fi_atraso, fi_recebido, fi_valor_recebido
        # print(resultado[i][1])
        i = i + 1
    # print(resultado)
    # print(res_filtrado)
    # print(len(resultado))
    conexao.close()
    return res_filtrado


# FIM GERA RELATORIO FINANCEIRO MENSAL

# Função gera relatório de não pagadores - para substituir a rel_nao_pagadores
def mensalidades_relatorio_devidas(mesano):
    """
    Relatório de alunos com dívidas no mês.
    :param mesano:
    :return: índice, nome do aluno, valor da parcela atrasada, dia do vencimento
    """
    # Retorna índice, nome do aluno, valor da parcela atrasada, dia do vencimento
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('SELECT al_index, al_nome FROM Alunos WHERE al_ativo = "S"')
    alunos = c.fetchall()
    dados = (mesano, 0)
    resultado = []
    lista = []
    conexao.close()
    conexao = sqlite3.connect(mdbfile)
    c = conexao.cursor()
    for idx, x in enumerate(alunos):
        nometabela = 'mens_' + str(x[0])
        comando = 'SELECT me_valor, ' \
                  'me_diaven FROM ' + nometabela + ' WHERE me_mesano LIKE ? AND me_pg = ?'
        c.execute(comando, dados)
        lista = c.fetchone()
        print(lista)
        if lista:
            temp = list(lista)
            temp.insert(0, x[0])
            temp.insert(1, x[1])
            resultado.append(temp)
    print(resultado)
    conexao.close()
    return resultado


# FUNCAO GERA RELATORIO NAO PAGADORES
def rel_nao_pagadores(mesano, opcao):  # todo pra que serve essa função?
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    # c.execute('SELECT al_nome,al_endereco,al_telefone01,al_telefone02,al_email,al_dt_matricula,al_dt_vencto FROM
    # Alunos WHERE al_index = ?', (indice,))

    # c.execute('SELECT fi_data_pgto,fi_atraso,fi_valor_rec,fi_recebido FROM Financeiro fin JOIN Alunos al on
    # fin.fi_nome = al.al_index WHERE al.al_index = ?', (indice,))

    # mesano = ('%'+ mesano + '%')
    #    c.execute('SELECT fi_nome,* FROM Financeiro WHERE fi_data_pgto LIKE ?', (mesano,))
    # print(mesano)
    # c.execute('SELECT al_nome,al_ultimopagto,al_valmens FROM Alunos WHERE al_ultimopagto NOT like ?',(mesano,))
    c.execute('SELECT al_nome,al_ultimopagto,al_valmens,al_dt_vencto FROM Alunos')
    resultado_par = c.fetchall()
    conexao.close()
    # data_mesano = datetime.strptime(mesano, '%m/%Y')
    # data_mesano = data_mesano - relativedelta(months=2)
    mesanant = ''
    mes = mesano[0:2]  # SEPARA O MES
    ano = mesano[3:7]  # SEPARA O ANO
    if mes == '01':  # TESTA PARA JANEIRO
        mes = 12
        ano = int(ano) - 1
    # mesanterior = str(mes) + '/' + str(ano)
    else:
        mescalc = int(mes) - 1  # TIRA 1 DO MES (TRANSFORMA NO MES ANTERIOR)
        # mesanterior = str(mescalc) + '/' + ano  # TRANSFORMA mesanterior EM STRING MES + ANO
        mescalc = int(mes) - 1  # SUBTRAI MAIS UM DO MES (TRANSFORMA NO AN ANTERIOR)
        mesanant = str(mescalc) + '/' + ano
    # print(mesano2)
    # dmesanterior = datetime.strptime(mesanterior, '%m/%Y').date()
    dmesanant = datetime.strptime(mesanant, '%m/%Y').date()
    dmesatual = datetime.strptime(mesano, '%m/%Y').date()
    # dif = data1 - data2
    # print(str(dif))
    resultado = []
    i = 0
    while i < len(resultado_par):
        # print(resultado_par[i])
        if resultado_par[i][1] is not None:
            temp2 = resultado_par[i][1]
            temp2 = temp2[3:10]
            # print('temp2 ',temp2)
            # print('data2 ',data2)
            datatemp = datetime.strptime(temp2, '%m/%Y').date()
            # print('Datatemp ', datatemp)
            if opcao == 'atual':
                if datatemp < dmesatual and datatemp == dmesanant:
                    # print('datatemp<data2')
                    resultado.append(resultado_par[i])
                    # print(resultado)
            if opcao == 'anteriores':
                if datatemp < dmesatual:
                    # print('datatemp<data2')
                    resultado.append(resultado_par[i])
                    # print(resultado)
        else:
            resultado.append(resultado_par[i])
        i = i + 1

    return resultado


# FIM GERA RELATORIO NAO PAGADORES

# FUNCAO INSERE DADOS NA TABELA FINANCEIRO
def insere_dados_financeiros(indice, datapagto, atraso, valrec, recpor):
    dadosinsert = [indice, datapagto, atraso, valrec, recpor]
    secinsert = [datapagto, indice]
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute('INSERT INTO Financeiro (fi_nome,fi_data_pgto,fi_atraso,fi_valor_rec,fi_recebido) VALUES (?,?,?,?,?)',
              dadosinsert)
    c.execute('UPDATE Alunos SET al_ultimopagto = ? WHERE al_index = ?', secinsert)
    conexao.commit()
    # print('tamanho resultado')
    # print(len(resultado))
    conexao.close()


# FINAL FUNCAO INSERE DADOS NA TABELA FINANCEIRO


# FUNCAO BUSCA ALUNO POR INDICE
def buscar_aluno_index(indice):
    conexao = sqlite3.connect(dbfile)
    c = conexao.cursor()
    c.execute(
        'SELECT al_index,al_nome,al_endereco,al_telefone01,al_cpf,al_email,al_dt_matricula,al_dt_vencto,al_valmens,'
        'al_ultimopagto,al_ativo,al_op_desc,al_op_dias,al_desc FROM Alunos WHERE al_index = ?',
        (indice,))
    #    c.execute('SELECT * from Alunos WHERE al_index = ?', (indice,))
    resultado = c.fetchone()
    # print('resultado')
    # print(resultado)
    conexao.close()
    return resultado


# FINAL FUNCAO BUSCA ALUNO POR INDICE

# INICIO SPLASH SCREEN
def splashscreen():
    imgfile = imagem
    display_time_milliseconds = 2000  # DISPLAY_TIME_MILLISECONDS
    sg.Window('Window Title', [[sg.Image(filename=imgfile)]],
              transparent_color=sg.theme_background_color(),  # transparent_color='#f0f0f0'
              no_titlebar=True).read(timeout=display_time_milliseconds, close=True)  # keep_on_top=True


# FINAL SPLASH SCREEN

# FUNCAO CALCULA DIFERENCA ENTRE DATAS RETORNA DIAS
def diferenca_datas(date1, date2):
    d1 = datetime.strptime(date1, "%d/%m/%Y")
    d2 = datetime.strptime(date2, "%d/%m/%Y")
    resultado = (d2 - d1).days
    if resultado <= 0:
        resultado = 0
    else:
        resultado = abs(resultado)
    return resultado


# FINAL FUNCAO CALCULA DIFERENCA ENTRE DATAS RETORNA DIAS

# FUNCAO GERA DATA VENCIMENTO
def geravencto(datavencto):  # EDITANDO - CHECAR SE ESSA FUNCAO FAZ SENTIDO
    tdata = date.today()
    mesano = tdata.strftime("%m/%Y")
    datavencimento = (str(datavencto) + '/' + mesano)
    # print(datavencimento)
    return datavencimento


# FINAL FUNCAO GERA DATA VENCIMENTO

# FUNCAO ORGANIZA TABELA
# extraída de Demo_Table_Element_Header_or_Cell_Clicks.py
# que é parte do pacote de programas de demonstração da PySimpleGUI
def sort_table(table, cols):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table


def mes_extenso(mes_int, opcao):
    # converte o número de um mês (int) para o nome
    # opcao: 0 ret. mes extenso, 1 retorna mes abreviado
    resultado = ''
    if opcao == 0:
        resultado = dtt.date(1900, mes_int, 1).strftime('%B')
    elif opcao == 1:
        resultado = dtt.date(1900, mes_int, 1).strftime('%b')
    resultado = resultado.capitalize()
    return resultado


def mes_numero(mes_str):
    # converte o nome de um mês em número
    if len(mes_str) > 3:
        int_tmp = strptime(mes_str, '%B').tm_mon
    else:
        int_tmp = strptime(mes_str, '%b').tm_mon
    if int_tmp in (1, 2, 3, 4, 5, 6, 7, 8, 9):
        resultado = '0' + str(int_tmp)
    else:
        resultado = str(int_tmp)
    return resultado


# gera o backup automático dos bancos de dados do sistema
def backup_auto():
    nomedapasta = 'db'
    enderecopai = os.getcwd()
    data = datetime.now()
    data = data.strftime("%d-%m-%Y")
    pastabkp = str(sg.user_settings_get_entry('-bkpautopasta-')) + '/'
    nomearq = 'database-' + data
    arquivo = pastabkp + nomearq
    try:
        shutil.make_archive(base_name=arquivo, root_dir=enderecopai,
                            base_dir=nomedapasta, format='zip', logger=logger)
        data = datetime.now()
        data = data.strftime("%d/%m/%Y")
        sg.user_settings_set_entry('-lastbackup-', data)
        return 0
    except Exception as err:
        logger.error(err, exc_info=True)
        print('Erro na criação do arquivo compactado.')
        return 1


# def validar_data(date_text):
#    try:
#        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
#            raise ValueError
#        return True
#    except ValueError:
#        return False

# janela configurar opções de treino
class Opcoes_treino:
    row = []
    dados = []

    def __init__(self):
        self.primeiro = True
        self.desfazapaga = False
        self.editando = False
        self.linha = None
        self.values = None
        self.event = None
        self.tabela_header = ['Índice', 'Descrição', 'Dias', 'Valor']
        self.tabela_larg = [5, 25, 5, 10]
        self.col_direita = sg.Column([[
            sg.Frame('Opções', [
                [sg.B('Editar', k='-EDITAR-', s=(8, 1))],
                [sg.B('Desfazer', k='-DESFAZER-', s=(8, 1), disabled=True)],
                [sg.B('Limpar', k='-LIMPAR-', s=(8, 1))],
                [sg.B('Gravar', k='-SALVAR-', s=(8, 1))],
                [sg.B('Excluir', k='-APAGAR-', s=(8, 1))],
            ])
        ]])
        self.col_esquerda = sg.Column([[
            sg.Frame('Treinos disponíveis (clique para editar)', [
                [sg.Table(values=opcao_ler(),
                          visible_column_map=[True, True, True, True],
                          headings=self.tabela_header, max_col_width=20,
                          auto_size_columns=False,
                          col_widths=self.tabela_larg,
                          justification='left',
                          num_rows=8,
                          key='-TABELA-',
                          enable_events=True,
                          expand_x=True,
                          expand_y=True,
                          bind_return_key=True,
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                          tooltip='Selecione um campo e clique em editar, alterar ou excluir.'
                          )],
            ])
        ]])
        self.col_abaixo = sg.Column([[
            sg.Frame('Editar', [
                [sg.T('Descrição:', s=(8, 1)), sg.I(k='-DESCRICAO-', s=(40, 1)),
                 sg.T('Dias por semana:'), sg.I(k='-DIASSEMANA-', s=(5, 1))],
                [sg.T('Valor R$:', s=(8, 1)), sg.I(k='-VALOR-', s=(10, 1))],
            ])
        ]])

        self.layout = [
            [sg.Text('Opções de treino', font='_ 25', key='-TITULO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [self.col_esquerda,
             self.col_direita],
            [self.col_abaixo],
            [sg.Push(), sg.Button('Fechar', k='-FECHAR-')],
            [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],
            [sg.StatusBar('Selecione um item da lista para editar/excluir, ou crie um novo.')]
        ]

        self.window = sg.Window('Opções de treino', self.layout,
                                finalize=True, )

        self.window['-EXPAND-'].expand(True, True, True)

    def run(self):
        # converter o valor em moeda antes de popular a tabela.
        tabela_tmp2 = []
        tabela_tmp = opcao_ler()
        for idx, x in enumerate(tabela_tmp):
            tabela_tmp2.append([x[0], x[1], x[2], locale.currency(float(x[3]))])
        if self.primeiro:
            self.window['-TABELA-'].update(values=tabela_tmp2)
            self.primeiro = False
        while True:
            self.event, self.values = self.window.read()
            # print('event: ', self.event)
            # print('values: ', self.values)

            if self.event == '-TABELA-':
                self.row = self.values[self.event]
                self.dados = self.window['-TABELA-'].Values
                # print('row: ', self.row)

            if self.event == '-ATUALIZA-':
                tabela_tmp2 = []
                tabela_tmp = opcao_ler()
                for idx, x in enumerate(tabela_tmp):
                    tabela_tmp2.append([x[0], x[1], x[2], locale.currency(float(x[3]))])
                self.window['-TABELA-'].update(values=tabela_tmp2)

            if self.event == '-EDITAR-':
                if len(self.row) != 0:
                    self.editando = True
                    self.linha = self.dados[self.row[0]]
                    self.window['-DESCRICAO-'].update(self.linha[1])
                    self.window['-DIASSEMANA-'].update(self.linha[2])
                    self.window['-VALOR-'].update(self.linha[3])
                    self.window['-DESFAZER-'].update(disabled=False)
                else:
                    sg.popup('Selecione um registro na tabela.')

            if self.event == '-DESFAZER-':
                self.window['-DESCRICAO-'].update(self.linha[1])
                self.window['-DIASSEMANA-'].update(self.linha[2])
                self.window['-VALOR-'].update(self.linha[3])
                self.window['-DESFAZER-'].update(disabled=True)
                # self.editando = False

            if self.event == '-LIMPAR-':
                self.window['-DESCRICAO-'].update('')
                self.window['-DIASSEMANA-'].update('')
                self.window['-VALOR-'].update('')
                self.editando = False

            if self.event == '-SALVAR-':
                valor = self.window['-VALOR-'].get()
                if valor != '':
                    valor = valor.translate({ord(c): None for c in "R$ "})
                else:
                    sg.popup('Campo valor não pode ser vazio.')
                if self.window['-DESCRICAO-'].get() == '':
                    sg.popup('Campo descrição vazio.')
                elif self.window['-DIASSEMANA-'].get() == '':
                    sg.popup('Campo dias por semana vazio.')
                elif self.window['-VALOR-'].get() == '':
                    sg.popup('Campo valor vazio.')
                elif self.values['-VALOR-'].rstrip() != '' and not \
                        re.fullmatch(regexDinheiro, valor):
                    sg.popup('Valor deve ser no formato xxx,xx.')
                else:
                    valor = valor.replace(',', '.')
                    if self.editando:
                        indice = self.linha[0]
                        opcao_escreve(indice, self.window['-DESCRICAO-'].get(),
                                      self.window['-DIASSEMANA-'].get(), valor)
                    else:
                        opcao_escreve(99, self.window['-DESCRICAO-'].get(),
                                      self.window['-DIASSEMANA-'].get(), valor)
                    self.window['-DESCRICAO-'].update('')
                    self.window['-DIASSEMANA-'].update('')
                    self.window['-VALOR-'].update('')
                    self.window['-DESFAZER-'].update(disabled=True)
                    self.editando = False
                    self.window.write_event_value('-ATUALIZA-', '')
                    # self.window['-TABELA-'].update(values=opcao_ler())
                    self.primeiro = True

            if self.event == '-APAGAR-':
                if len(self.row) != 0:
                    opcao, _ = sg.Window('Continuar?', [[sg.T('Tem certeza?')],
                                                        [sg.Yes(s=10, button_text='Sim'),
                                                         sg.No(s=10, button_text='Não')]], disable_close=True,
                                         modal=True).read(close=True)
                    if opcao == 'Sim':
                        self.linha = self.dados[self.row[0]]
                        opcao_apagar(self.linha[0])
                        self.primeiro = True
                        self.window['-DESCRICAO-'].update('')
                        self.window['-DIASSEMANA-'].update('')
                        self.window['-VALOR-'].update('')
                        self.editando = False
                        self.window.write_event_value('-ATUALIZA-', '')
                else:
                    sg.popup('Selecione um registro na tabela.')

            if self.event in (sg.WIN_CLOSED, '-FECHAR-'):
                break

        self.window.close()


# JANELA CONFIGURACOES

class Configuracoes:
    """
    DEFINICOES:
    '-cormensatraso-' = COR DE REALCE DO ALUNO COM MENSALIDADE EM ATRASO NA TABELA PRINCIPAL
    '-corplanofinal-' = COR DE REALCE DO ALUNO COM PLANO PRESTES A ACABAR NA TABELA PRINCIPAL
    '-coralunoinativo-' = COR DE REALCE DO ALUNO MARCADO COMO INATIVO NA TABELA PRINCIPAL
    """

    def __init__(self):
        self.values = None
        self.event = None
        self.layframe = [
            [sg.T('Descrição:'), sg.I(s=(50, 1), k='-DESC-')],
            [sg.T('Período (meses):'), sg.I(s=(4, 1), k='-PER-'),
             sg.T('Valor (porc.):'), sg.I(s=(4, 1), k='-VAL-')],
        ]
        self.coluna1 = [
            [sg.Frame('Cores de realce', layout=[
                # [sg.T('Mensalidade em atraso:'), sg.I(k='-CMENS-', s=(6, 1)), sg.ColorChooserButton('Cor')],
                # [sg.T('Plano prestes a acabar:'), sg.I(k='-CPLA-', s=(6, 1)), sg.ColorChooserButton('Cor')]
                [sg.T('Mensalidade em atraso:'), sg.Push(), sg.I(k='-CMENS-', s=(8, 1)), sg.B('Cor', k='-COR1-')],
                [sg.T('Plano prestes a acabar:'), sg.Push(), sg.I(k='-CPLA-', s=(8, 1)), sg.B('Cor', k='-COR2-')],
                [sg.T('Alunos inativos:'), sg.Push(), sg.I(k='-CINA-', s=(8, 1)), sg.B('Cor', k='-COR3-')]
            ])]
        ]

        self.coluna2 = [
            [sg.Frame('Financeiro', layout=[
                [sg.T('Desconto bom pagador')],
                [sg.T('Digite o valor em Reais ou 0,00 para não usar o desconto.')],
                [sg.T('Valor R$:'), sg.I(k='-VALOR-', s=(20, 1)), sg.Push(), sg.B('Gravar', k='-GRAVA-')],
                [sg.HorizontalSeparator()],
                [sg.T('Desconto família')],
                [sg.T('Digite o valor em porcentagem.')],
                [sg.T('Valor %:'), sg.I(k='-DESCONTOFAMILIA-', s=(20, 1)),
                 sg.Push(), sg.B('Gravar', k='-GRAVADESCONTOFAMILIA-')]
            ])]
        ]

        self.coluna3 = [
            [sg.Frame('Backup', layout=[
                [sg.Checkbox('Fazer backup automático?', k='-FAZBKPAUTO-')],
                [sg.T('Período: a cada'), sg.I(k='-PER-', s=(5, 1)), sg.T('dias.')],
                [sg.T('Pasta de backup:'), sg.Push(), sg.I(k='-PASTA-', s=(50, 1)), sg.FolderBrowse('Procurar...')],
                [sg.T('Não esqueça de gravar suas alterações:'), sg.B('Gravar', k='-GRAVABACKUP-')],
                [sg.T('Teste o funcionamento do backup se estiver ativado:'), sg.B('Fazer backup agora', k='-FAZBKP-')]

            ])]
        ]

        self.layout = [
            [sg.Image(source=icones[1]),
             sg.Text('Configurações do sistema', font='_ 25', key='-TITULO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.Column(self.coluna2), sg.VPush(), sg.Column(self.coluna1)],
            [sg.Column(self.coluna3)],
            # [sg.Frame('', self.layframe)],
            [sg.Push(), sg.Button('Fechar', k='-FECHAR-')]
        ]

        self.window = sg.Window('Configurações', self.layout,
                                finalize=True, )  # modal=True,

    def run(self):
        while True:
            tmp = sg.user_settings_get_entry('-cormensatraso-')
            self.window['-CMENS-'].update(tmp)
            self.window['-CMENS-'].update(background_color=tmp)
            tmp = sg.user_settings_get_entry('-corplanofinal-')
            self.window['-CPLA-'].update(tmp)
            self.window['-CPLA-'].update(background_color=tmp)
            tmp = sg.user_settings_get_entry('-coralunoinativo-')
            self.window['-CINA-'].update(tmp)
            self.window['-CINA-'].update(background_color=tmp)
            tmp = sg.user_settings_get_entry('-valordesconto-')
            tmp2 = str(tmp) + '0'
            tmp2 = tmp2.replace('.', ',')
            self.window['-VALOR-'].update(tmp2)
            tmp = sg.user_settings_get_entry('-valordescontofamilia-', 0.1)
            self.window['-DESCONTOFAMILIA-'].update(tmp)
            tmp = sg.user_settings_get_entry('-bkpautomatico-', False)
            self.window['-FAZBKPAUTO-'].update(tmp)
            tmp = sg.user_settings_get_entry('-bkpperiodo-')
            self.window['-PER-'].update(tmp)
            tmp = sg.user_settings_get_entry('-bkpautopasta-')
            self.window['-PASTA-'].update(tmp)

            self.event, self.values = self.window.read()

            if self.event == '-COR1-':
                cor = cores.popup_color_chooser('Dark Blue 3')
                self.window['-CMENS-'].update(cor)
                self.window['-CMENS-'].update(background_color=cor)
                valor = self.window['-CMENS-'].get()
                # print(valor)
                sg.user_settings_set_entry('-cormensatraso-', valor)

            if self.event == '-COR2-':
                cor = cores.popup_color_chooser('Dark Blue 3')
                self.window['-CPLA-'].update(cor)
                self.window['-CPLA-'].update(background_color=cor)
                valor = self.window['-CPLA-'].get()
                # print(valor)
                sg.user_settings_set_entry('-corplanofinal-', valor)

            if self.event == '-COR3-':
                cor = cores.popup_color_chooser('Dark Blue 3')
                self.window['-CINA-'].update(cor)
                self.window['-CINA-'].update(background_color=cor)
                valor = self.window['-CINA-'].get()
                # print(valor)
                sg.user_settings_set_entry('-coralunoinativo-', valor)

            if self.event == '-GRAVA-':
                valor = self.values['-VALOR-'].rstrip()
                if self.values['-VALOR-'].rstrip() == '':
                    sg.popup('Campo valor do desconto não pode ser vazio.')
                elif self.values['-VALOR-'].rstrip() != '' and not \
                        re.fullmatch(regexDinheiro, self.values['-VALOR-'].rstrip()):
                    sg.popup('Valor do desconto deve ser no formato xxx,xx')
                else:
                    valor = valor.replace(',', '.')
                    valorf = float(valor)
                    sg.user_settings_set_entry('-valordesconto-', valorf)
                    sg.popup('Valor do desconto alterado com sucesso.')

            if self.event == '-GRAVADESCONTOFAMILIA-':
                desconto = self.values['-DESCONTOFAMILIA-']
                if desconto == '':
                    sg.popup('Desconto família não pode ser vazio.')
                elif not re.fullmatch(regexDesconto, desconto):
                    sg.popup('Desconto família deve ser no formato x.xx')
                else:
                    sg.user_settings_set_entry('-valordescontofamilia-', desconto)

            if self.event == '-GRAVABACKUP-':
                if self.values['-FAZBKPAUTO-']:
                    sg.user_settings_set_entry('-bkpautomatico-', True)
                    sg.user_settings_set_entry('-bkpperiodo-', self.values['-PER-'])
                    sg.user_settings_set_entry('-bkpautopasta-', self.values['-PASTA-'])
                else:
                    sg.user_settings_set_entry('-bkpautomatico-', False)

            if self.event == '-FAZBKP-':
                if self.values['-FAZBKPAUTO-']:
                    resultado = backup_auto()
                    if resultado == 0:
                        sg.popup('Backup realizado com sucesso.')
                    else:
                        sg.popup('Falha no backup.')
                else:
                    sg.popup('O backup automático deve estar ativado.')

            if self.event in (sg.WIN_CLOSED, '-FECHAR-'):
                break
        self.window.close()


# ################################################
# CLASSE ADERIR_PLANOS - INICIO
# ################################################
class Aderir_planos:
    indicealuno = None
    nomealuno = None
    tabela2header = ['Data', 'Descrição', 'Valor']
    tabela2larg = [8, 20, 8]
    first = True
    dados = None
    planoindice = None  # indice do plano
    planomeses = 0  # meses de duração
    planodescricao = ''  # descrição do plano
    planoinicio = ''  # data de início da validade do plano (string)
    planofim = ''  # data de final do plano (string)
    valordesc = 0.0
    v_mens_com_desconto = 0.0  # mensalidade com desconto
    v_total_com_desconto = 0.0  # soma das mensalidades no período + desconto
    v_normal_total = 0.0  # valor total sem desconto
    diftot = 0.0  # diferença do valor total - desconto
    difmens = 0.0  # desconto na mensalidade (no mês)
    datainicio = None
    datafim = None

    def __init__(self):
        self.values = None
        self.event = None
        self.row = []

        self.colunacobranca = [[sg.Frame('', [
            [sg.T('Plano escolhido:'), sg.T('', k='-NOMEPLANO-', font='_ 10 bold')],
            [sg.Table(values=[],
                      visible_column_map=[True, True, True],
                      headings=self.tabela2header, max_col_width=20,
                      auto_size_columns=False,
                      col_widths=self.tabela2larg,
                      justification='left',
                      num_rows=5,
                      key='-TABELAVALORES-',
                      enable_events=True,
                      expand_x=True,
                      expand_y=True,
                      bind_return_key=True,
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE
                      )],
            [sg.Push(), sg.T('Total:', font='_ 18'), sg.I(k='-VALORFINAL-', s=(10, 1), font='_ 18',
                                                          justification='right')],
            [sg.Push(), sg.B('Imprimir', k='-IMPRIMIR-'), sg.B('Receber', k='-RECEBER-')]
        ], size=(480, 350)), ]]

        self.coluna1 = [
            [sg.T('Normal')],
            [sg.T('Mens.:', s=(6, 1)), sg.I(k='-VLNORM-', s=(10, 1), disabled=True)],
            [sg.T('Total:', s=(6, 1)), sg.I(k='-VLNORMT-', s=(10, 1), disabled=True)]
        ]
        self.coluna2 = [
            [sg.T('Plano')],
            [sg.T('Mens.:', s=(6, 1)), sg.I(k='-VLMEN-', s=(10, 1), disabled=True)],
            [sg.T('Total:', s=(6, 1)), sg.I(k='-VALOR-', s=(10, 1), disabled=True)]
        ]
        self.coluna3 = [
            [sg.T('Economia')],
            [sg.T('Mens.:', s=(6, 1)), sg.I(k='-DMEN-', s=(10, 1), disabled=True)],
            [sg.T('Total:', s=(6, 1)), sg.I(k='-DTOT-', s=(10, 1), disabled=True)]
        ]

        self.colunaprincipal = [[
            sg.Frame('', layout=[
                [sg.T('Inscrito:', s=(6, 1)),
                 sg.I('Nenhum', s=(30, 1), k='-INSCRITO-', disabled=True),
                 sg.Push(), sg.T('Período:', s=(6, 1)),
                 sg.I(k='-PERIODO-', s=(15, 1), disabled=True)],
                [sg.T('Início:', s=(6, 1)),
                 sg.I(k='-INICIO-', s=(15, 1), disabled=True), sg.Push(),
                 sg.T('Final:', s=(6, 1)),
                 sg.I(k='-FINAL-', s=(15, 1), disabled=True)],
                [sg.Push(), sg.T('Valores para comparação'), sg.Push()],
                [sg.Frame('',
                          layout=[
                              [sg.Column(self.coluna1, element_justification='left',
                                         justification='left'),
                               sg.Column(self.coluna2, element_justification='left',
                                         justification='center'),  # , size=(80, 1)
                               sg.Column(self.coluna3, element_justification='left',
                                         justification='right')]],
                          element_justification='center')],
                [sg.HorizontalSeparator(k='-SEP-')],
                [sg.T('Planos disponíveis - clique para selecionar')],
                [sg.Table(values=planos_ler(),
                          headings=['No.', 'Plano', 'Período', 'Valor'],
                          visible_column_map=[False, True, True, True],
                          # sg.Table(values=busca_dadosinfo_financeiros(self.indiceinfo),headings=self.tblheadinfo,
                          key='-TABELAPL-',
                          # max_col_width=10,
                          auto_size_columns=False,
                          col_widths=[0, 30, 10, 10],
                          # pad=(5,5,5,5),
                          num_rows=3,
                          # def_col_width=5,
                          # alternating_row_color='lightblue4',
                          # selected_row_colors='black on lightblue1',
                          enable_events=True,
                          expand_x=False,
                          expand_y=True
                          # select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                          # enable_click_events=True
                          )], [sg.Push(),
                               sg.B('Simular', k='-SIM-'),
                               sg.B('Inscrever (vai para cobrança)', k='-INSC-')]
            ], size=(480, 350))]]

        self.layout = [
            [sg.Text('Planos', font='_ 25', key='-TITULO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.T(k='-NOMEALUNO-')],
            [sg.Column(self.colunaprincipal, k='-COL1-'),
             sg.Column(self.colunacobranca, k='-COL2-', visible=False)],
            [sg.Push(), sg.B('Voltar', k='-VOLTAR-', disabled=True), sg.B('Fechar', k='-FECHAR-')],
        ]

        self.window = sg.Window('Planos', self.layout,
                                finalize=True
                                )
        # self.colunapane.expand(True, True) #  modal=True,

    def run(self):
        while True:
            if self.first:
                self.window['-TABELAPL-'].Update(values=planos_ler())
                self.window['-NOMEALUNO-'].Update(value=self.nomealuno)
                self.first = False

            self.event, self.values = self.window.read()

            if self.event == sg.WIN_CLOSED or self.event == '-FECHAR-':
                break

            if self.event == '-TABELAPL-':
                self.row = self.values[self.event]
                # print(self.row)
                self.dados = self.window['-TABELAPL-'].Values

            if self.event == '-SIM-':
                if len(self.row) != 0:
                    self.window['-INSCRITO-'].update(self.dados[self.row[0]][1])
                    self.window['-PERIODO-'].update(self.dados[self.row[0]][2])
                    tmpmonths = int(self.dados[self.row[0]][2])
                    self.planoindice = int(self.dados[self.row[0]][0])
                    self.planomeses = tmpmonths
                    self.planodescricao = self.dados[self.row[0]][1]
                    if buscar_aluno_index(self.indicealuno)[13] in (
                            0.0, None, ''):  # retorna se o aluno tem plano família
                        valorstr = buscar_aluno_index(self.indicealuno)[8]  # retorna valor da mensalidade
                        valorstr = valorstr.replace(',', '.')
                        self.valordesc = float(valorstr) * float(self.dados[self.row[0]][3])
                        self.v_mens_com_desconto = float(valorstr) - self.valordesc
                        self.v_normal_total = float(valorstr) * float(self.dados[self.row[0]][2])
                    else:  # se plano familia não estiver vazia
                        valorstr = buscar_aluno_index(self.indicealuno)[8]
                        valorstr = valorstr.replace(',', '.')
                        self.v_mens_com_desconto = float(valorstr)
                        self.v_normal_total = float(valorstr) * float(self.dados[self.row[0]][2])
                        sg.popup('Aluno já com desconto família: não é possível acumular descontos.')
                    self.v_total_com_desconto = self.v_mens_com_desconto * tmpmonths
                    # diferença entre a mensalidade completa e com desconto
                    self.difmens = float(valorstr) - self.v_mens_com_desconto
                    # diferença entre os valores totais
                    self.diftot = self.v_normal_total - float(self.v_total_com_desconto)
                    self.window['-VLMEN-'].update(locale.currency(self.v_mens_com_desconto))
                    # self.windowinfo['-VLNORM-'].update(str(buscar_aluno_index(self.indiceinfo)[8]))
                    self.window['-VLNORM-'].update(locale.currency(float(valorstr)))
                    self.window['-VLNORMT-'].update(locale.currency(self.v_normal_total))
                    ultima_mensalidade = mensalidades_ultima_paga(self.indicealuno)
                    # print('ultima mensalidade: ', ultima_mensalidade)
                    # print('aluno ', self.indicealuno)

                    if ultima_mensalidade == 0:
                        diavencto = buscar_aluno_index(self.indicealuno)[7]
                        self.datainicio = datetime.now()
                        self.datainicio = self.datainicio + relativedelta(day=int(diavencto))
                        self.window['-INICIO-'].update(datetime.strftime(self.datainicio, '%d/%m/%Y'))
                        self.planoinicio = datetime.strftime(self.datainicio, '%d/%m/%Y')
                        self.datafim = self.datainicio + relativedelta(months=+tmpmonths)
                        self.window['-FINAL-'].update(datetime.strftime(self.datafim, '%d/%m/%Y'))
                        self.planofim = datetime.strftime(self.datafim, '%d/%m/%Y')
                    else:
                        # print('ultima_mensalidade[0] : ', ultima_mensalidade)
                        # print('mesano hj ', datetime.strftime(datetime.now(), '%m/%Y'))
                        if ultima_mensalidade[0] >= datetime.strftime(datetime.now(), '%m/%Y'):
                            # se existem mensalidades que não foram pagas, o plano começa a partir daí
                            # print('entrou no if de string')
                            diavencto = buscar_aluno_index(self.indicealuno)[7]
                            dtstr = diavencto + '/' + ultima_mensalidade[0]
                            dataultimamens = datetime.strptime(dtstr, '%d/%m/%Y')
                            # diferenca = dataultimamens - datetime.now()
                            self.datainicio = dataultimamens + relativedelta(months=1)
                            # self.datainicio = self.datainicio + relativedelta(day=int(diavencto))
                            self.datafim = self.datainicio + relativedelta(months=+tmpmonths)
                            self.window['-INICIO-'].update(datetime.strftime(self.datainicio, '%d/%m/%Y'))
                            self.planoinicio = datetime.strftime(self.datainicio, '%d/%m/%Y')
                            self.window['-FINAL-'].update(datetime.strftime(self.datafim, '%d/%m/%Y'))
                            self.planofim = datetime.strftime(self.datafim, '%d/%m/%Y')
                        else:
                            # print('entrou no else de string')
                            diavencto = buscar_aluno_index(self.indicealuno)[7]
                            self.datainicio = datetime.now()
                            self.datainicio = self.datainicio + relativedelta(day=int(diavencto))
                            self.planoinicio = datetime.strftime(self.datainicio, '%d/%m/%Y')
                            self.window['-INICIO-'].update(datetime.strftime(self.datainicio, '%d/%m/%Y'))
                            self.datafim = self.datainicio + relativedelta(months=+tmpmonths)
                            self.planofim = datetime.strftime(self.datafim, '%d/%m/%Y')
                            self.window['-FINAL-'].update(datetime.strftime(self.datafim, '%d/%m/%Y'))
                        # print('bizarro ', ultima_mensalidade[0] >= datetime.strftime(datetime.now(), '%m/%Y'))
                    self.window['-VALOR-'].update(locale.currency(self.v_total_com_desconto))
                    self.window['-DMEN-'].update(locale.currency(self.difmens))
                    self.window['-DTOT-'].update(locale.currency(self.diftot))
                    # print('self.v_mens_com_desconto ', self.v_mens_com_desconto)
                else:
                    sg.Popup('Selecione um registro na tabela.')

            if self.event == '-INSC-':
                if len(self.row) != 0:
                    opcao, _ = sg.Window('Continuar?', [[sg.T('Inscreve o aluno no plano?')],
                                                        [sg.Yes(s=10, button_text='Sim'),
                                                         sg.No(s=10, button_text='Não')]],
                                         disable_close=True, modal=True).read(close=True)
                    if opcao == 'Sim':
                        self.window.write_event_value('-SIM-', 'teste')
                        self.window['-COL1-'].update(visible=False)
                        self.window['-COL2-'].update(visible=True)
                        self.window['-VOLTAR-'].update(disabled=False)
                        self.window['-NOMEPLANO-'].update(value=self.dados[self.row[0]][1])
                        self.planoindice = self.dados[self.row[0]][0]
                        # Alimentando a tabela valores:
                        tabelatmp = [[datetime.strftime(datetime.now(), '%d/%m/%Y'),
                                      self.dados[self.row[0]][1], locale.currency(self.v_normal_total)],
                                     [datetime.strftime(datetime.now(), '%d/%m/%Y'),
                                      'Desconto', locale.currency(-abs(self.diftot))]]
                        self.window['-TABELAVALORES-'].update(values=tabelatmp)
                        self.window['-VALORFINAL-'].update(value=locale.currency(self.v_total_com_desconto))

                    else:
                        sg.Popup('Selecione um registro na tabela.')

            if self.event == '-RECEBER-':
                controle = True
                print(self.dados[self.row[0]][2])
                idx = 0
                while idx < int(self.dados[self.row[0]][2]):
                    datatmp = self.datainicio + relativedelta(months=+idx)
                    mesano = datetime.strftime(datatmp, '%m/%Y')
                    insercao = mensalidades_insere_plano(
                        self.indicealuno, mesano, buscar_aluno_index(self.indicealuno)[7], self.v_mens_com_desconto,
                        datetime.strftime(datetime.now(), '%d/%m/%Y'),
                        round(self.difmens, True), 0.0, self.v_mens_com_desconto,
                        1, 0, self.dados[self.row[0]][0], self.dados[self.row[0]][1], self.planoinicio, self.planofim
                    )
                    print('Resultado: ', insercao)
                    # print('indice do aluno ', self.indicealuno)
                    # print('mesano ', mesano)
                    # print('diaven ', buscar_aluno_index(self.indicealuno)[7])
                    # print('valor ', self.v_mens_com_desconto)
                    # print('datapagto ', datetime.strftime(datetime.now(), '%d/%m/%Y'))
                    # print('vlrmulta (desconto) ', round(self.difmens, True))
                    # print('vlrextras ', '0.0')
                    # print('valorpago ', self.v_mens_com_desconto)
                    # print('pg, 1')
                    # print('atraso, 0')
                    # print('plindex ', self.dados[self.row[0]][0])
                    # print('desc. plano ', self.dados[self.row[0]][1])
                    # print('inicio plano ', self.planoinicio)
                    # print('fim plano ', self.planofim)
                    idx = idx + 1
                sg.popup('Aluno inscrito no plano com sucesso.')

            if self.event == '-VOLTAR-':
                self.window['-COL2-'].update(visible=False)
                self.window['-COL1-'].update(visible=True)
                self.window['-VOLTAR-'].update(disabled=True)

        self.window.close()


# JANELA ALTERA PLANOS
class Editar_planos:
    row = []
    dados = []
    linha = []
    editando = False

    def __init__(self):
        self.values = None
        self.event = None
        self.col_direita = sg.Column([[
            sg.Frame('Opções', [
                [sg.B('Editar', k='-EDITAR-', s=(8, 1))],
                [sg.B('Desfazer', k='-DESFAZER-', s=(8, 1), disabled=True)],
                [sg.B('Limpar', k='-LIMPAR-', s=(8, 1))],
                [sg.B('Gravar', k='-SALVAR-', s=(8, 1))],
                [sg.B('Excluir', k='-APAGAR-', s=(8, 1))],
            ])
        ]])
        self.col_esquerda = sg.Column([[
            sg.Frame('', [
                [sg.T('Planos são divididos em descrição, período e valor.')],
                [sg.T('Período é a duração do plano em meses.')],
                [sg.T('Valor é a porcentagem de desconto oferecida.')],
                [sg.T('Planos existentes:')],
                [sg.Table(planos_ler(),
                          headings=['I', 'Descrição', 'Período', 'Valor'],
                          visible_column_map=[False, True, True, True],
                          col_widths=[0, 50, 5, 5],
                          num_rows=4,
                          enable_events=True,
                          k='-TPLANOS-',
                          expand_y=True,
                          expand_x=True,
                          right_click_selects=True,
                          right_click_menu=['&Right', ['Editar']]
                          )],
            ])
        ]])
        self.col_inferior = sg.Column([[
            sg.Frame('', [
                [sg.T('Descrição:'), sg.I(s=(50, 1), k='-DESCRICAO-')],
                [sg.T('Período (meses):'), sg.I(s=(4, 1), k='-PERIODO-'),
                 sg.T('Valor (porc.):'), sg.I(s=(4, 1), k='-VALOR-')],
            ])
        ]])
        self.layout = [
            [sg.Text('Opções de planos', font='_ 25', key='-TITULO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [self.col_esquerda,
             self.col_direita],
            [self.col_inferior],
            [sg.Push(), sg.Button('Fechar', k='-FECHAR-')],
            [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],
            [sg.StatusBar('Selecione um item da lista para editar/excluir, ou crie um novo.')]
        ]

        self.window = sg.Window('Planos', self.layout,
                                finalize=True
                                )
        self.window['-EXPAND-'].expand(True, True, True)

    def run(self):
        while True:
            self.event, self.values = self.window.read()

            if self.event == '-TPLANOS-':
                self.row = self.values[self.event]
                self.dados = self.window['-TPLANOS-'].Values

            if self.event == '-ATUALIZA-':
                self.window['-TPLANOS-'].update(values=planos_ler())

            if self.event == '-EDITAR-':
                if len(self.row) != 0:
                    self.editando = True
                    self.linha = self.dados[self.row[0]]
                    self.window['-DESCRICAO-'].update(self.linha[1])
                    self.window['-PERIODO-'].update(self.linha[2])
                    self.window['-VALOR-'].update(self.linha[3])
                    self.window['-DESFAZER-'].update(disabled=False)
                else:
                    sg.popup('Selecione um registro na tabela.')

            if self.event == '-DESFAZER-':
                self.window['-DESCRICAO-'].update(self.linha[1])
                self.window['-PERIODO-'].update(self.linha[2])
                self.window['-VALOR-'].update(self.linha[3])
                self.window['-DESFAZER-'].update(disabled=True)

            if self.event == '-LIMPAR-':
                self.window['-DESCRICAO-'].update('')
                self.window['-PERIODO-'].update('')
                self.window['-VALOR-'].update('')
                self.editando = False

            if self.event == '-SALVAR-':
                if self.window['-DESCRICAO-'].get() == '':
                    sg.popup('Campo descrição vazio.')
                elif self.window['-PERIODO-'].get() == '':
                    sg.popup('Campo período vazio.')
                elif self.window['-VALOR-'].get() == '':
                    sg.popup('Campo valor vazio.')
                else:
                    if self.editando:
                        indice = self.linha[0]
                        planos_grava(indice, self.window['-DESCRICAO-'].get(),
                                     self.window['-PERIODO-'].get(), self.window['-VALOR-'].get())
                    else:
                        planos_grava(99, self.window['-DESCRICAO-'].get(),
                                     self.window['-PERIODO-'].get(), self.window['-VALOR-'].get())
                    self.window['-DESCRICAO-'].update('')
                    self.window['-PERIODO-'].update('')
                    self.window['-VALOR-'].update('')
                    self.window['-DESFAZER-'].update(disabled=True)
                    self.editando = False
                    self.window.write_event_value('-ATUALIZA-', '')

            if self.event == '-APAGAR-':
                if len(self.row) != 0:
                    opcao, _ = sg.Window('Continuar?', [[sg.T('Tem certeza?')],
                                                        [sg.Yes(s=10, button_text='Sim'),
                                                         sg.No(s=10, button_text='Não')]], disable_close=True,
                                         modal=True).read(close=True)
                    if opcao == 'Sim':
                        self.linha = self.dados[self.row[0]]
                        planos_apagar(self.linha[0])
                        self.window['-DESCRICAO-'].update('')
                        self.window['-PERIODO-'].update('')
                        self.window['-VALOR-'].update('')
                        self.window['-DESFAZER-'].update(disabled=True)
                        self.editando = False
                        self.window.write_event_value('-ATUALIZA-', '')
                else:
                    sg.popup('Selecione um registro na tabela.')

            if self.event == sg.WIN_CLOSED or self.event == '-FECHAR-':
                break
        self.window.close()


# INICIO JANELA AJUDA
class Ajuda:
    nomearquivo = ''

    def __init__(self):
        self.values = None
        self.event = None
        self.layout = [
            [sg.Text('Ajuda do programa', font='_ 25', key='-TITULO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.Multiline(disabled=True, size=(50, 20), k='-TEXTO-')],
            [sg.Button('Fechar', k='-FECHAR-')]
        ]

        self.window = sg.Window('Ajuda', self.layout,
                                default_element_size=(12, 1), finalize=True, modal=True,
                                location=(10, 10))

    def run(self):
        while True:
            self.window['-TEXTO-'].update(abrir_texto(self.nomearquivo))
            # janelahtml = HTMLScrolledText(self.window.TKroot, html=abrir_texto(self.nomearquivo), width=60, height=20)
            # janelahtml.pack()
            self.event, self.values = self.window.read()
            if self.event == sg.WIN_CLOSED or self.event == '-FECHAR-':
                break
        self.window.close()


# FINAL JANELA AJUDA

# INICIO JANELA SOBRE

class Sobre:
    nomearquivo = 'sobre.txt'

    def __init__(self):
        self.values = None
        self.event = None
        self.layout = [
            [sg.Image(source=imagem_peq), sg.Text('Sistema de gerenciamento de alunos', font='_ 20', key='-TITULO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.Text('')],
            [sg.Multiline(disabled=True, size=(80, 20), k='-TEXTO-')],
            [sg.Push(), sg.Button('Fechar', k='-FECHAR-')]
        ]

        self.window = sg.Window('Sobre...', self.layout,
                                default_element_size=(12, 1), finalize=True, )

    def run(self):
        while True:
            self.window['-TEXTO-'].update(abrir_texto(self.nomearquivo))
            # janelahtml = HTMLScrolledText(self.window.TKroot, html=abrir_texto(self.nomearquivo), width=60, height=20)
            # janelahtml.pack()
            self.event, self.values = self.window.read()
            if self.event == sg.WIN_CLOSED or self.event == '-FECHAR-':
                break
        self.window.close()


# FINAL JANELA SOBRE

# INICIO LEMBRETES

class Lembretes:

    def __init__(self):
        self.values = None
        self.event = None
        self.layout = [
            [sg.Text('Lembretes', font='_ 25', key='-TITULO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.T('Data para o lembrete:'), sg.I(k='-DATA-', s=(10, 1)),
             sg.CalendarButton('Data', locale='pt_BR', format='%d/%m/%Y',
                               month_names=meses, day_abbreviations=dias)],
            [sg.Multiline(size=(30, 10), k='-TEXTO-')],
            [sg.Push(), sg.B('Gravar', k='-GRAVA-')],
            [sg.Push(), sg.Button('Fechar', k='-FECHAR-')]
        ]

        self.window = sg.Window('Lembretes', self.layout,
                                default_element_size=(12, 1), finalize=True, modal=True,
                                location=(150, 50))

    def run(self):
        while True:
            self.event, self.values = self.window.read()

            if self.event == sg.WIN_CLOSED or self.event == '-FECHAR-':
                break
        self.window.close()


# FINAL LEMBRETES

# CLASSE GRAFICO
class grafico_mensal:
    larg_barra = 50  # width of each bar
    espacamento = 30  # space between each bar
    borda = 3  # offset from the left edge for first bar
    tamanho = (400, 300)
    primeiro = True

    def __init__(self):
        self.graph_value = None
        self.event = None
        self.values = None
        self.graph = None
        self.pagos = None
        self.npagos = None
        # self.layoutframe = [
        #     [sg.Graph(self.tamanho, (0, -self.tamanho[0] // 2), (self.tamanho[0] // 2, self.tamanho[1] // 2),
        #               k='-GRAFICO-', background_color='beige')]
        # ]
        self.layoutframe = [
            [sg.Graph(self.tamanho, (0, 0),
                      (self.tamanho[0], self.tamanho[1]),
                      k='-GRAFICO-', background_color='beige', drag_submits=True)]
        ]
        self.layout = [
            [sg.Image(source=icones[0]),
             sg.Text('Mensalidades em gráfico', font='_ 25', key='-NOMEALUNO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.Text('Percentual de mensalidades')],
            [sg.T('Mês:'), sg.Combo(meses, key='-MES-', default_value=mesatual(), enable_events=True, readonly=True)],

            # [sg.Text('Mês:'), sg.I(k='-MES-', s=(10, 1))],
            [sg.Text('Mensalidades recebidas:'),
             sg.Text('', k='-REC-', background_color='green', text_color='white'),
             sg.Push(), sg.Text('Mensalidades em haver:'),
             sg.Text('', k='-HAV-', background_color='red', text_color='white')],
            [sg.Frame('Gráfico', layout=self.layoutframe)],
            [sg.Push(), sg.Button('Voltar', k='-VOLTAR-')]
        ]

        self.window = sg.Window('Gráfico', self.layout, enable_close_attempted_event=True, finalize=True)
        self.graph: sg.Graph = self.window['-GRAFICO-']

    def run(self):
        while True:
            if self.primeiro:
                self.window['-MES-'].update(value=mesatual())
                porcentagens = mensalidades_porcentagem(datetime.strftime(datetime.now(), '%m/%Y'))
                self.pagos = porcentagens[0]
                self.npagos = porcentagens[1]
                self.window['-REC-'].update(str(round(self.pagos)) + '%')
                self.window['-HAV-'].update(str(round(self.npagos)) + '%')
                self.graph.erase()

                # self.graph_value = 100

                # self.graph.draw_rectangle(top_left=(self.espacamento + self.borda, self.graph_value),
                #                           bottom_right=(self.espacamento + self.borda + self.larg_barra, 0),
                #                           fill_color='green', line_width=0)
                esquerda = 140
                self.graph.draw_rectangle(top_left=(esquerda, self.pagos + 75),
                                          bottom_right=(esquerda + self.larg_barra, 75),
                                          fill_color='green', line_width=0)

                self.graph.draw_rectangle(top_left=(self.larg_barra + esquerda + self.espacamento, self.npagos + 75),
                                          bottom_right=(self.larg_barra + esquerda + self.larg_barra +
                                                        self.espacamento, 75), fill_color='red', line_width=0)
                self.graph.draw_text('Pagas', (esquerda + 24, 70), color='green')
                self.graph.draw_text('Não pagas', (esquerda + self.larg_barra + self.espacamento + 25, 70), color='red')
                self.primeiro = False

            self.event, self.values = self.window.read()
            # print(self.event, self.values)

            mes = '0'
            if self.values['-MES-'].rstrip() == 'Janeiro':
                mes = '01'
            elif self.values['-MES-'].rstrip() == 'Fevereiro':
                mes = '02'
            elif self.values['-MES-'].rstrip() == 'Março':
                mes = '03'
            elif self.values['-MES-'].rstrip() == 'Abril':
                mes = '04'
            elif self.values['-MES-'].rstrip() == 'Maio':
                mes = '05'
            elif self.values['-MES-'].rstrip() == 'Junho':
                mes = '06'
            elif self.values['-MES-'].rstrip() == 'Julho':
                mes = '07'
            elif self.values['-MES-'].rstrip() == 'Agosto':
                mes = '08'
            elif self.values['-MES-'].rstrip() == 'Setembro':
                mes = '09'
            elif self.values['-MES-'].rstrip() == 'Outubro':
                mes = '10'
            elif self.values['-MES-'].rstrip() == 'Novembro':
                mes = '11'
            elif self.values['-MES-'].rstrip() == 'Dezembro':
                mes = '12'

            if self.event == '-MES-':
                # print(mes + datetime.strftime(datetime.now(), '/%Y'))
                porcentagens = mensalidades_porcentagem(mes + datetime.strftime(datetime.now(), '/%Y'))
                self.pagos = porcentagens[0]
                self.npagos = porcentagens[1]
                self.window['-REC-'].update(str(round(self.pagos)) + '%')
                self.window['-HAV-'].update(str(round(self.npagos)) + '%')
                self.graph.erase()
                esquerda = 140
                self.graph.draw_rectangle(top_left=(esquerda, self.pagos + 75),
                                          bottom_right=(esquerda + self.larg_barra, 75),
                                          fill_color='green', line_width=0)

                self.graph.draw_rectangle(top_left=(self.larg_barra + esquerda + self.espacamento, self.npagos + 75),
                                          bottom_right=(self.larg_barra + esquerda + self.larg_barra +
                                                        self.espacamento, 75), fill_color='red', line_width=0)
                self.graph.draw_text('Pagas', (esquerda + 24, 70), color='green')
                self.graph.draw_text('Não pagas', (esquerda + self.larg_barra + self.espacamento + 25, 70), color='red')

            if self.event in (sg.WIN_CLOSE_ATTEMPTED_EVENT, '-VOLTAR-'):
                break
        self.window.close()


"""
# INICIO RECEBE MENSALIDADE
class Recebe:
    indicealuno = 2
    tam_texto = (10, 1)
    tam_input = (10, 1)
    diasatraso = 0
    nome_aluno = ''

    def __init__(self):
        self.values = None
        self.event = None
        self.layout = [
            [sg.Text('nome', font='_ 25', key='-NOMEALUNO-')],
            # [sg.Text('nome',relief='sunken', font=('italic'),key='-NOMEALUNO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.Text('Vencimento:', size=self.tam_texto), sg.Input(k='-DATAVEN-', size=self.tam_input, disabled=True),
             sg.Push(), sg.Text('Valor:', size=self.tam_texto),
             sg.Input(k='-VALMENS-', size=self.tam_input, disabled=True)],
            [sg.Text('Pagamento:', size=self.tam_texto, ),
             sg.Input(k='-DATAPAGTO-', size=self.tam_input, default_text=datetime.strftime(datetime.now(), '%d/%m/%Y')),
             sg.CalendarButton('Data', locale='pt_BR', format='%d/%m/%Y', month_names=meses, day_abbreviations=dias),
             sg.Push(), sg.Text('Atraso:', size=self.tam_texto), sg.Input(k='-ATRASO-', size=self.tam_input)],
            [sg.Text('Recebido:', self.tam_texto), sg.Input(k='-VALREC-', size=self.tam_input),
             sg.Push(), sg.Text('Multa:', self.tam_texto), sg.Input(k='-VALMULTA-', size=self.tam_input)],
            [sg.Text('Usuário:', size=self.tam_texto), sg.Input(k='-USUARIO-', size=(18, 1), default_text='Andréia'),
             sg.Push(), sg.Checkbox('Aplica multa?', default=False, k='-APLMULTA-', enable_events=True)],
            [sg.Button('Calcular', k='-CALC-'), sg.Button('Confirma', k='-CONF-', bind_return_key=True),
             sg.Button('Gera para impressão', k='-IMPRIME-', disabled=True), sg.Button('Voltar', k='-VOLTAR-')],
            [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],
            [sg.StatusBar('Pronto para receber dados', k='-STATUS-', s=10, expand_y=True)]
        ]
        # JANELA RECEBE MENSALIDADE
        self.window = sg.Window('Recebimento de mensalidade', self.layout,
                                default_element_size=(12, 1), finalize=True, modal=True,
                                disable_minimize=True)  # modal=True,

    def run(self):
        while True:
            self.window['-NOMEALUNO-'].update(str(buscar_aluno_index(self.indicealuno)[1]))
            self.nome_aluno = str(buscar_aluno_index(self.indicealuno)[1])
            self.window['-VALMENS-'].update(str(buscar_aluno_index(self.indicealuno)[8]))
            self.window['-DATAVEN-'].update(str(buscar_aluno_index(self.indicealuno)[7]))
            # diasatraso = diferenca_datas(geravencto(self.values['-DATAVEN-'].rstrip()),
            #                              self.values['-DATAPAGTO-'].rstrip())
            diasatraso = diferenca_datas(geravencto(str(buscar_aluno_index(self.indicealuno)[7])),
                                         datetime.strftime(datetime.now(), '%d/%m/%Y'))
            self.window['-ATRASO-'].update(diasatraso)
            # self.window['-VALREC-'].update(str(buscar_aluno_index(self.indicealuno)[8]))
            vlrfnstr = str(buscar_aluno_index(self.indicealuno)[8])
            if diasatraso > 5:
                valorstr = str(buscar_aluno_index(self.indicealuno)[8])
                # print(resultado[idx])
                valorstr = valorstr.replace(',', '.')
                vlrmulta = float(valorstr) * 0.02
                vlrmultastr = str(vlrmulta)
                vlrmultastr = vlrmultastr.replace('.', ',')
                vlrmultastr = vlrmultastr + '0'
                valorfin = float(valorstr) + vlrmulta
                vlrfnstr = str(valorfin)
                vlrfnstr = vlrfnstr.replace('.', ',')
                vlrfnstr = vlrfnstr + '0'
                self.window['-VALMULTA-'].update(vlrmultastr)
            self.event, self.values = self.window.read()
            if self.event in (sg.WIN_CLOSED, '-VOLTAR-'):
                break

            if self.event == '-APLMULTA-':
                if self.values['-APLMULTA-']:
                    self.window['-VALREC-'].update(vlrfnstr)
                else:
                    self.window['-VALREC-'].update(str(buscar_aluno_index(self.indicealuno)[8]))

            if self.event == '-CALC-':
                if self.values['-DATAPAGTO-'].rstrip() == '':
                    sg.Popup('Não foi preenchida a data de pagamento.')
                else:
                    diasatraso = diferenca_datas(geravencto(self.values['-DATAVEN-'].rstrip()),
                                                 self.values['-DATAPAGTO-'].rstrip())
                    self.window['-ATRASO-'].update(diasatraso)
                    if diasatraso > 5:
                        valorstr = str(buscar_aluno_index(self.indicealuno)[8])
                        # print(resultado[idx])
                        valorstr = valorstr.replace(',', '.')
                        vlrmulta = float(valorstr) * 0.02
                        vlrmultastr = str(vlrmulta)
                        vlrmultastr = vlrmultastr.replace('.', ',')
                        vlrmultastr = vlrmultastr + '0'
                        valorfin = float(valorstr) + vlrmulta
                        vlrfnstr = str(valorfin)
                        vlrfnstr = vlrfnstr.replace('.', ',')
                        vlrfnstr = vlrfnstr + '0'
                        self.window['-VALMULTA-'].update(vlrmultastr)
                    if self.values['-APLMULTA-']:
                        self.window['-VALREC-'].update(vlrfnstr)
                    else:
                        self.window['-VALREC-'].update(str(buscar_aluno_index(self.indicealuno)[8]))

                    # self.window['-IMPRIME-'].update(disabled=False)

            if self.event == '-CONF-':
                if self.values['-DATAPAGTO-'].rstrip() == '':
                    sg.Popup('Não foi preenchida a data de pagamento.')
                else:
                    diasatraso = diferenca_datas(geravencto(self.values['-DATAVEN-'].rstrip()),
                                                 self.values['-DATAPAGTO-'].rstrip())
                    self.window['-ATRASO-'].update(diasatraso)
                    # print(self.indicealuno,self.values['-DATAPAGTO-'].rstrip(),diasatraso,self.values['-VALREC-'].rstrip(),self.values['-USUARIO-'].rstrip())
                    insere_dados_financeiros(self.indicealuno, self.values['-DATAPAGTO-'].rstrip(), diasatraso,
                                             self.values['-VALREC-'].rstrip(), self.values['-USUARIO-'].rstrip())
                    self.window['-IMPRIME-'].update(disabled=False)
                    self.window['-STATUS-'].update('Inserido com sucesso.')
                    # sg.Popup('Dados inseridos com sucesso.')

            if self.event == '-IMPRIME-':
                if self.values['-DATAPAGTO-'].rstrip() == '':
                    sg.Popup('Não foi preenchida a data de pagamento.')
                else:
                    diasatraso = diferenca_datas(geravencto(self.values['-DATAVEN-'].rstrip()),
                                                 self.values['-DATAPAGTO-'].rstrip())
                    self.window['-ATRASO-'].update(diasatraso)
                    gera_recibo_pdf(self.nome_aluno, self.values['-VALREC-'].rstrip(),
                                    self.values['-DATAPAGTO-'].rstrip(), self.values['-DATAVEN-'].rstrip(),
                                    self.values['-ATRASO-'].rstrip(), self.values['-USUARIO-'].rstrip())
                    self.window.perform_long_operation(lambda: os.system('\"' + pdfviewer + '\" ' + arq_recibo),
                                                       '-FUNCTION COMPLETED-')
                    # os.system(arq_recibo)
                    break
        self.window.close()
"""


# FINAL RECEBE MENSALIDADE

#########################################
# RECEBE MENSALIDADE V3
#########################################
class Pagamentos:
    indicealuno = None
    nomealuno = None
    mesano = None
    diavencimento = None
    datapagto = None
    atraso = None
    vendas = None
    datavencimento = None
    datasvendas = []
    desconto_familia = float  # busca o desconto familia se existir
    valorfinal = float  # guarda o valor final calculado, para ser gravado na tabela mensalidades
    valordesconto = float  # valor do desconto, gravado em mensalidade - me_vlrmulta
    valorvendas = float  # valor total de possiveis vendas a ser gravado
    valormensalidade = float  # valor da mensalidade como consta na tabela mensalidades
    valor_desconto_f = float  # valor do desconto família calculado de acordo com a mensalidade
    valoresextras = 0.0
    linhatabela = None
    tabela1header = ['Vencimento', 'Data', 'Valor']
    tabela1larg = [0, 8, 8]
    tabela2header = ['Indice', 'Data', 'Descrição', 'Valor']
    tabela2larg = [0, 8, 20, 8]
    row = []
    recebido = False

    def mensalidade_antiga(self):
        layout = [
            [sg.T('Entre com os dados da mensalidade')],
            [sg.T('Data:'), sg.I(datetime.strftime(datetime.now(), '%d/%m/%Y'), s=(10, 1), k='-DATAMANTIGA-'),
             sg.CalendarButton('Data do vencimento', locale='pt_BR', format='%d/%m/%Y',
                               month_names=meses,
                               day_abbreviations=dias,
                               tooltip='Clique para mudar a data')],
            [sg.T('Valor:'), sg.I(buscar_aluno_index(self.indicealuno)[8], k='-VALMANTIGA-', s=(10, 1))],
            [sg.T(''), sg.Push(), sg.B('Criar', k='-CRIAMANTIGA-'), sg.B('Sair', k='-SAIR-')]
        ]
        return sg.Window('Mensalidade antiga', layout, finalize=True)

    def __init__(self):
        self.coluna1 = sg.Column([[sg.Frame('', [
            [sg.T('Mensalidades')],
            [sg.Table(
                values=[],
                visible_column_map=[False, True, True],
                headings=self.tabela1header, max_col_width=25,
                auto_size_columns=False,
                col_widths=self.tabela1larg,
                justification='left',
                num_rows=5,
                key='-TABELAMENSALIDADE-',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                bind_return_key=True,
                select_mode=sg.TABLE_SELECT_MODE_BROWSE
            )],
        ], size=(250, 180)), ],
      [
          sg.Frame('', [
              # sg.T('Data do pagamento:'),
              [sg.CalendarButton('Data do pagamento', locale='pt_BR', format='%d/%m/%Y',
                                 month_names=meses,
                                 day_abbreviations=dias,
                                 tooltip='Clique para mudar a data'), sg.Push(),
               sg.Input(k='-DATAPAGTO-', size=(10, 1),
                        default_text=datetime.strftime(datetime.now(), '%d/%m/%Y'),
                        enable_events=True),
               ],
              # [sg.T('Valor recebido:'), sg.Push(),
              # sg.I(s=(10, 1), k='-VALORRECEBIDO-', justification='right',
              #      focus=True, enable_events=True)],
              # [sg.T('Troco:'), sg.Push(),
              #  sg.I(s=(10, 1), k='-TROCO-', justification='right')],
          ], size=(250, 100)),
      ]])

        self.coluna2 = sg.Column([[sg.Frame('', [
            [sg.T('Valores a receber')],
            [sg.Table(values=[],
                      visible_column_map=[False, True, True, True],
                      headings=self.tabela2header, max_col_width=20,
                      auto_size_columns=False,
                      col_widths=self.tabela2larg,
                      justification='left',
                      num_rows=5,
                      key='-TABELAVALORES-',
                      enable_events=True,
                      expand_x=True,
                      expand_y=True,
                      bind_return_key=True,
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE
                      )],
            [sg.Push(), sg.T('Alterar valor:', s=(10, 1)),
             sg.I(k='-VALORALT-', s=(10, 1), justification='right'),
             sg.B('Alterar', k='-ALTERA-', s=(12, 1))],
            [sg.Push(), sg.T('Total:', font='_ 10 bold', s=(10, 1)), sg.I(k='-VALORFINAL-', s=(10, 1), font='_ 10 bold',
                                                                          justification='right'),
             sg.B('Receber <F5>', k='-RECEBER-', font='_ 10 bold', s=(12, 1))],
            [sg.Push(), sg.B('Imprimir recibo <F6>', k='-IMPRIMIR-', disabled=True), ]
        ], size=(400, 287)), ]])

        self.coluna3 = sg.Column([[sg.Frame('', [
            [sg.B('Criar mensalidade antiga', k='-ANTIGA-'),
             sg.B('Perdoar mensalidade', k='-PERDOA-'),
             sg.Push(), sg.Button('Voltar', k='-VOLTAR-')]
        ], size=(672, 40)), ]])

        self.layout = [
            [sg.Image(source=icones[2]),
             sg.Text('nome', font='_ 25', key='-NOMEALUNO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.vtop([self.coluna1, self.coluna2])],
            [self.coluna3]
        ]

        self.window = sg.Window('Recebimento de mensalidade', self.layout,
                                default_element_size=(12, 1), finalize=True
                                )
        self.window.bind('<F5>', '-RECEBER-')
        self.window.bind('<F6>', '-IMPRIMIR-')

    def run(self):
        tabelatmp = mensalidades_a_pagar(self.indicealuno)
        for idx, x in enumerate(tabelatmp):
            x[2] = locale.currency(float(x[2]))
        self.window['-TABELAMENSALIDADE-'].update(values=tabelatmp)
        # self.window['-VALORRECEBIDO-'].set_focus()
        self.window['-NOMEALUNO-'].update(self.nomealuno)

        while True:

            self.event, self.values = self.window.read()

            if self.event in (sg.WIN_CLOSED, '-VOLTAR-'):
                break

            if self.event == '-TABELAMENSALIDADE-':
                self.row = self.values[self.event]
                print(self.row)
                if len(self.row) != 0:
                    self.linhatabela = self.row
                    self.dados = self.window['-TABELAMENSALIDADE-'].Values
                    print(self.dados[self.row[0]])
                    tblmensalidade = self.dados[self.row[0]]
                    # print(tblmensalidade)
                    self.mesano = tblmensalidade[1]
                    self.mesano = self.mesano[3:]
                    self.diavencimento = tblmensalidade[0]
                    mensalidade = tblmensalidade[2].translate({ord(c): None for c in "R$"})
                    mensalidade = mensalidade.replace(',', '.')
                    self.valormensalidade = float(mensalidade)
                    self.valorfinal = self.valormensalidade
                    self.valordesconto = sg.user_settings_get_entry('-valordesconto-')
                    datapagto = datetime.strptime(self.window['-DATAPAGTO-'].get(), '%d/%m/%Y')
                    datavencimento = datetime.strptime(tblmensalidade[1], '%d/%m/%Y')
                    self.datavencimento = tblmensalidade[1]
                    self.datapagto = self.window['-DATAPAGTO-'].get()
                    entradastabela = [[99, self.window['-DATAPAGTO-'].get(),
                                       ('Mensalidade de ' + self.mesano), locale.currency(self.valormensalidade)]]
                    # print('datapagto ', datapagto)
                    # print('datavencimento ', datavencimento)
                    self.atraso = diferenca_datas(tblmensalidade[1], self.window['-DATAPAGTO-'].get())
                    self.desconto_familia = buscar_aluno_index(self.indicealuno)[13]
                    print(self.desconto_familia)
                    if self.desconto_familia != 0.0 and self.desconto_familia:
                        print('entrou no desconto familia')
                        self.valor_desconto_f = float(self.valormensalidade) * float(self.desconto_familia)
                        print('valor desc fam: ', self.valor_desconto_f)
                        self.valorfinal = float(self.valormensalidade) - float(self.valor_desconto_f)
                        print('valor final: ', self.valorfinal)
                        entradastabela.append([50, self.window['-DATAPAGTO-'].get(),
                                               'Desconto família', locale.currency(self.valor_desconto_f)])
                    if self.valordesconto != 0.0:
                        if datapagto < datavencimento:
                            self.valorfinal = float(self.valormensalidade) - self.valordesconto
                            entradastabela.append([50, self.window['-DATAPAGTO-'].get(),
                                                   'Desconto', locale.currency(self.valordesconto)])
                    self.vendas = venda_busca(self.indicealuno)
                    if self.vendas:
                        for idx, x in enumerate(self.vendas):
                            if x[4] == 'SIM':
                                self.datasvendas.append(x[1])
                                tmp = x[3].replace(',', '.')
                                entradastabela.append([x[0], x[1], x[2], locale.currency(float(tmp))])
                                self.valoresextras = self.valoresextras + float(tmp)
                                self.valorfinal = self.valorfinal + float(tmp)
                    self.window['-TABELAVALORES-'].update(values=entradastabela)
                    self.window['-VALORFINAL-'].update(locale.currency(self.valorfinal))
                    self.window['-VALORALT-'].update(value='')
                else:
                    pass
                # EDITANDO3
                # print(self.valorfinal)

            if self.event == '-DATAPAGTO-':
                self.window.write_event_value('-TABELAMENSALIDADE-', self.linhatabela)

            if self.event == '-ALTERA-':
                if self.values['-VALORALT-'] != '':
                    valoralt = self.values['-VALORALT-']
                    valoralt = valoralt.translate({ord(c): None for c in "R$ "})
                    if re.fullmatch(regexDinheiro, valoralt):
                        opcao, _ = sg.Window('Continuar?', [[sg.T('Tem certeza que deseja alterar o valor final?')],
                                                            [sg.Yes(s=10, button_text='Sim'),
                                                             sg.No(s=10, button_text='Não')]], disable_close=True,
                                             modal=True).read(close=True)
                        if opcao == 'Sim':
                            valoralt = valoralt.replace(',', '.')
                            self.window['-VALORFINAL-'].update(locale.currency(float(valoralt)))
                            self.valorfinal = float(valoralt)

            if self.event == '-RECEBER-':
                if len(self.row) != 0:
                    resultadotmp = mensalidades_insere(self.indicealuno, self.mesano,
                                                       self.diavencimento, self.valormensalidade,
                                                       self.datapagto, self.valordesconto,
                                                       self.valoresextras, self.valorfinal, 1, self.atraso)
                    if resultadotmp in (0, 1):
                        sg.popup('Mensalidade recebida com sucesso.')
                        for idx, x in enumerate(self.datasvendas):
                            print('datasvendas x ', x)
                            venda_recebe(self.indicealuno, x)
                        tabelatmp = mensalidades_a_pagar(self.indicealuno)
                        for idx, x in enumerate(tabelatmp):
                            x[2] = locale.currency(float(x[2]))
                        self.window['-TABELAMENSALIDADE-'].update(values=tabelatmp)
                        # self.window['-TABELAVALORES-'].update(values=[])
                        # self.window['-VALORFINAL-'].update(value='')
                        self.recebido = True
                        self.window['-IMPRIMIR-'].update(disabled=False)
                    if resultadotmp == 2:
                        sg.popup('Esta mensalidade já foi paga.')
                else:
                    sg.popup('Selecione uma mensalidade.')

            if self.event == '-IMPRIMIR-':
                if self.recebido:
                    pdfgen.gera_recibo_pdf(self.nomealuno, locale.currency(self.valorfinal),
                                           self.datapagto, self.datavencimento, str(self.atraso), 'Andréia')
                    self.window.perform_long_operation(
                        lambda: os.system('\"' + pdfviewer + '\" ' + pdfgen.arq_recibo),
                        '-FUNCTION COMPLETED-')
                    self.recebido = False
                    # self.window['-IMPRIMIR-'].update(disabled=True)
                else:
                    sg.popup('Nenhuma operação efetuada.')

            if self.event == '-PERDOA-':
                if len(self.row) != 0:
                    opcao, _ = sg.Window('Continuar?', [[sg.T('Tem certeza?')],
                                                        [sg.Yes(s=10, button_text='Sim'),
                                                         sg.No(s=10, button_text='Não')]], disable_close=True,
                                         modal=True).read(close=True)
                    if opcao == 'Sim':
                        tmp2 = mensalidades_insere(
                            self.indicealuno, self.mesano,
                            self.diavencimento, self.valormensalidade,
                            self.datapagto, self.valordesconto, self.valoresextras, 0.0, 1, self.atraso)
                        # if tmp2 == 1:
                        #     sg.popup('Mensalidade já existe.')
                        # elif tmp2 == 2:
                        #     sg.popup('Mensalidade já foi paga.')
                        # else:
                        #     sg.popup('Mensalidade inserida com sucesso.')
                        tabelatmp = mensalidades_a_pagar(self.indicealuno)
                        for idx, x in enumerate(tabelatmp):
                            x[2] = locale.currency(float(x[2]))
                        self.window['-TABELAMENSALIDADE-'].update(values=tabelatmp)
                        # self.window['-TABELAVALORES-'].update(values=[])
                        # self.window['-VALORFINAL-'].update(value='')
                        self.window['-IMPRIMIR-'].update(disabled=False)
                        self.recebido = True
                else:
                    sg.popup('Selecione um registro da tabela.')

            if self.event == '-ANTIGA-':
                self.windowa = self.mensalidade_antiga()
                while True:
                    self.eventa, self.valuesa = self.windowa.read()

                    if self.eventa == '-CRIAMANTIGA-':
                        if self.valuesa['-DATAMANTIGA-'] != '' and not \
                                re.fullmatch(regexData, self.valuesa['-DATAMANTIGA-']):
                            sg.popup('Data inválida.')
                        elif self.valuesa['-VALMANTIGA-'] != '' and not \
                                re.fullmatch(regexDinheiro, self.valuesa['-VALMANTIGA-']):
                            sg.popup('Valor inválido.')
                        else:
                            print('entrou no else pra criar a mensalidade')
                            mesano = self.valuesa['-DATAMANTIGA-'][3:]
                            mensantiga = self.valuesa['-VALMANTIGA-']
                            mensantiga = mensantiga.replace(',', '.')
                            tmp2 = mensalidades_insere(
                                self.indicealuno, mesano,
                                buscar_aluno_index(self.indicealuno)[7],
                                mensantiga, '', '', '', '', 0, '')
                            print('saída da mensalidade:', tmp2)
                            if tmp2 == 1:
                                sg.popup('Mensalidade já existe.')
                            elif tmp2 == 2:
                                sg.popup('Mensalidade já foi paga.')
                            else:
                                sg.popup('Mensalidade inserida com sucesso.')
                        tabelatmp = mensalidades_a_pagar(self.indicealuno)
                        for idx, x in enumerate(tabelatmp):
                            x[2] = locale.currency(float(x[2]))
                        self.window['-TABELAMENSALIDADE-'].update(values=tabelatmp)
                        break
                    if self.eventa in (sg.WIN_CLOSED, '-SAIR-'):
                        break

                self.windowa.close()

        self.window.close()


#########################################
# INICIO TELA PRINCIPAL
#########################################
class Principal:
    # ################################### CAD ALUNO
    formatodata = "%d/%m/%Y"
    res = True
    first = True
    # ################################### CAD ALUNO

    # ####################################TEMA
    # sg.theme(sg.user_settings_get_entry('-tema-'))
    # sg.change_look_and_feel('DarkBlue3')
    lista_temas = sg.list_of_look_and_feel_values()
    lista_temas.sort()
    # ####################################TEMA

    # ################################### MAIS INFO
    tblheadinfo = ['Indice', 'Mês', 'Data pagto.', 'Valor pago']
    largcolinfo = [0, 10, 10, 10]
    # tblvalores = ['01/01/2011','01/01/2011','Andréia']
    #    global indice
    indiceinfo = 0
    rowinfo = []
    dadosinfo = []
    planoinfo = True
    vtmp = True
    desconto = False
    vlrtotal = 0.0
    tmprecibo = []
    # ################################### MAIS INFO

    # ################################RECEBE VENDAS
    tblhdven = ['Indice', 'Data', 'Descrição', 'Valor']
    lcven = [0, 12, 25, 12]
    tmpdata = []

    planos_fim = True
    atrasados = True
    em_atraso = []
    periodo = 0
    planos_acabando = []
    planos_string = []
    opcaoselec = []
    largcol = [0, 30, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 20, 10, 10, 0, 0, 0, 20, 0, 0]
    coljust = ['r', 'l', 'l', 'r', 'r', 'l', 'r', 'r', 'r', 'r']
    tblhead = ['Indice', 'Nome', 'Endereço', 'Telefone', 'CPF', 'E-mail', 'Mat.', 'Venc.', 'Mensalidade',
               'Último pagto', 'Ativo', 'Ind.Plano', 'Plano', 'Início do plano', 'Fim do plano',
               'Renova', 'Pausa', 'Ind.Treino', 'Treino', 'Dias', 'Desc.']
    # "!" DESABILITA ITEM DO MENU, "&" TRANSFORMA EM ATALHO DO TECLADO, "'---'" CRIA UMA LINHA ENTRE OPCOES DO MENU
    menu_def = [
        ['&Arquivo', ['Adicionar aluno', 'Receber mensalidade',
                      'Informações do aluno', 'Financeiro', 'Lembretes', '---', '&Sair']],
        # 'Save::savekey',
        ['&Editar', ['Configurações', 'Mudar tema', '---', 'Editar opções de treino', 'Editar planos'], ],
        ['&Relatórios', ['Recebimento', 'Devedores', 'Gráfico', 'Lista de alunos(imprime)']],
        ['&Ferramentas', ['Backup parcial', 'Backup completo', ]],  # 'Administração', ['Limpar banco de dados']
        ['A&juda', ['Tela principal', 'Sobre...']], ]
    # ALTMENU
    right_click_menu = ['Unused', ['Abrir', '!&Click', '&Menu', 'E&xit', 'Properties']]

    row = []
    dados = []
    sort = True
    vendasrcb = None
    lbotao = (18, 1)

    def __init__(self):
        self.windowp = None
        self.layoutp = None
        self.indicep = None
        self.rowinfop = None
        self.dadosinfop = None
        self.valuesven = None
        self.eventven = None
        self.windowven = None
        self.layoutven = None
        self.indiceven = None
        self.indiceve = None
        self.dadosve = None
        self.rowve = None
        self.valuesv = None
        self.windowv = None
        self.layoutv = None
        self.indicev = None
        self.framelayout = None
        self.eventv = None
        self.cad_real = None
        self.values2 = None
        self.event2 = None
        self.window2 = None
        self.layout2 = None
        self.valuesinfo = None
        self.eventinfo = None
        self.windowinfo = None
        self.layoutinfo = None
        self.values3 = None
        self.event3 = None
        self.window3 = None
        self.layout3 = None
        self.values = None
        self.event = None
        # sg.theme(sg.user_settings_get_entry('-tema-'))
        # print(ler_todos_dados()[1])

        self.col_esquerda = sg.Column([[sg.Table(values=ler_todos_dados_ativos(),
                                                 visible_column_map=[False, True, False, False, False,
                                                                     False, False, False, False, False,
                                                                     False, False, True, True, True,
                                                                     False, False, False, True, False, False],
                                                 headings=self.tblhead, max_col_width=25,
                                                 auto_size_columns=False,
                                                 col_widths=self.largcol,
                                                 # display_row_numbers=True,
                                                 justification='left',
                                                 num_rows=18,
                                                 # alternating_row_color='lightblue4',
                                                 key='-TABELA-',
                                                 # selected_row_colors='black on lightblue1',
                                                 enable_events=True,
                                                 expand_x=True,
                                                 expand_y=True,
                                                 # enable_click_events=True,
                                                 # right_click_menu=self.right_click_menu,
                                                 # ESTE PARAMETRO CONTROLA O MENU DO BOTAO DIREITO
                                                 # select_mode=TABLE_SELECT_MODE_BROWSE,
                                                 bind_return_key=True
                                                 # ESTE PARAMETRO PERMITE A LEITURA DO CLIQUE DUPLO
                                                 )]], expand_x=True, expand_y=True)

        self.col_direita = sg.Column([[sg.Frame('Opções', [
            [sg.VPush()],
            [sg.Button('Adicionar alunos', key='-AD-', s=self.lbotao)],
            [sg.Button('Receber mensalidade', k='-RECEBE-', s=self.lbotao)],
            [sg.Button('Vender produtos', k='-VENDA-', s=self.lbotao)],
            [sg.Button('Receber produtos', k='-RECVENDA-', s=self.lbotao)],
            [sg.Button('Mais informações', k='-MAISINFO-', s=self.lbotao)],
            [sg.B('Planos', k='-ADERIRPLANOS-', s=self.lbotao)],
            [sg.B('Pausa', k='-PAUSA-', visible=False, s=self.lbotao)], [sg.VPush()]
        ], s=(150, 310), relief='solid', element_justification='center',
                                                vertical_alignment='center',
                                                expand_x=True, expand_y=True)]], expand_x=True, expand_y=True)

        self.col_inf_alt = sg.Column([[sg.Frame('', [
            [sg.Button('Adicionar alunos', key='-AD-', s=self.lbotao),
             sg.Button('Mais informações', k='-MAISINFO-', s=self.lbotao),
             sg.Button('Receber mensalidade', k='-RECEBE-', s=self.lbotao),
             sg.B('Planos', k='-ADERIRPLANOS-', s=self.lbotao),
             sg.Button('Vender produtos', k='-VENDA-', s=self.lbotao),
             sg.Button('Receber produtos', k='-RECVENDA-', s=self.lbotao),
             sg.B('Pausa', k='-PAUSA-', visible=False, s=self.lbotao)],
        ], )]], expand_x=True, expand_y=True)
        # relief = 'solid', element_justification = 'center',
        # vertical_alignment = 'center',
        # expand_x = True, expand_y = True

        self.col1 = [
            [sg.T('Bem vindo ao sistema Lótus')],
            [sg.T('Hoje é ' + datetime.strftime(datetime.now(), '%d de %B de %Y'))],
            [sg.Multiline('', s=(40, 15), k='-CAIXA-', background_color=sg.theme_background_color(),
                          text_color=sg.theme_text_color(), disabled=True)]
        ]
        self.frame1 = [
            [sg.T('    ', background_color=sg.user_settings_get_entry('-cormensatraso-')),
             sg.T('Mensalidade em atraso'),
             sg.T('    ', background_color=sg.user_settings_get_entry('-corplanofinal-')),
             sg.T('Plano próximo de acabar'),
             sg.T('    ', background_color=sg.user_settings_get_entry('-coralunoinativo-')),
             sg.T('Alunos inativos')
             ]
        ]

        self.layout = [
            [sg.Menu(self.menu_def, )],
            # [sg.Text(''), sg.Image(source=imagem_peq), sg.Text('Sistema de gerenciamento de alunos', font='_ 25'), ],
            [sg.Text(''), sg.Image(source=barra)],
            # [sg.HorizontalSeparator(k='-SEP-')],
            [sg.Column(self.col1, visible=False),
             self.col_esquerda,  # self.col_direita
             ],
            # [sg.Text('Local do click:'),sg.Input(k='-CLICKED-')],
            [sg.Push(), sg.Frame('', [
                [sg.Text('Buscar aluno por nome'), sg.Input(key='-BUSCAR-', focus=True),
                 sg.Button('Buscar', key='-BBUSCA-', bind_return_key=True),
                 sg.Button('Limpar', key='-LIMPA-'), sg.Button('Atualizar', k='-ATUALIZAR-'),
                 sg.Checkbox('Apenas alunos ativos', k='-ATIVOS-', default=True, enable_events=True)],
            ]), sg.Push()],
            [sg.Push(), self.col_inf_alt, sg.Push()],
            # [sg.Text('O que deseja fazer?')],

            [sg.Frame(title='Legenda', layout=self.frame1)],
            [sg.VPush()],
            [sg.Push(), sg.Button('Sair', k='-SAIR-')],
            [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],
            [sg.StatusBar('Obrigado por usar um software de código aberto!', k='-STATUS-', s=10, expand_y=True)]
        ]

        self.window = sg.Window('Gerenciamento de alunos', self.layout,
                                icon=icone, resizable=True, finalize=True,
                                enable_close_attempted_event=True,
                                location=sg.user_settings_get_entry('-location-', (None, None)))
        # ,right_click_menu=self.right_click_menu use_default_focus=True,
        self.window['-EXPAND-'].expand(True, True, True)
        # self.window.bind('<FocusOut>', '+FOCUS OUT+') #, self.window['-CLICKED-'].ButtonReboundCallback)
        # self.window['-CLICKED-'].bind('<FocusIn>', '+INPUT FOCUS+')
        self.window.bind('<F1>', 'Tela principal')
        # self.window.Maximize()

    def configura_tabela(self):
        indice = 0
        tmptabela = self.window['-TABELA-'].Values
        tabela_final = sort_table(tmptabela, (1,))
        self.window['-TABELA-'].Update(values=tabela_final)
        tmptabela = self.window['-TABELA-'].Values
        for idx, x in enumerate(tmptabela):
            atrasado = mensalidades_atraso(x[0])
            if atrasado:
                self.window['-TABELA-'].Update(
                    row_colors=[[indice, sg.user_settings_get_entry('-cormensatraso-')]])
            elif buscar_aluno_index(x[0])[10] == 'N':
                self.window['-TABELA-'].Update(
                    row_colors=[[indice, sg.user_settings_get_entry('-coralunoinativo-')]])
                # self.window['-CAIXA-'].print('Aluno ' + x[1] + ' em atraso.')
            else:
                self.window['-TABELA-'].Update(
                    row_colors=[[indice, 'white']])  # aqui deixei branco pq o tema não tem cor de fundo
            indice = indice + 1
        tmptabela = self.window['-TABELA-'].Values
        indice = 0
        for idx, x in enumerate(tmptabela):
            # print(x[0])
            dttemp = planos_acabando(x[0])
            # print(dttemp)
            if dttemp is not None and dttemp != '':
                dtatual = datetime.strptime(dttemp, '%d/%m/%Y')
                dthoje = datetime.now()
                deltafim = dtatual - dthoje
                # print(deltafim.days)
                diasfim = int(deltafim.days)
                if diasfim < 30:
                    self.window['-TABELA-'].Update(
                        row_colors=[[indice, sg.user_settings_get_entry('-corplanofinal-')]])
                    # self.window['-CAIXA-'].print(
                    #    'O plano de ' + x[1] + ' tem ' + str(diasfim) + ' dias para acabar.')
                self.planos_acabando.append((x[0], diasfim))
            indice = indice + 1
        # CHECA SE O ALUNO É INATIVO
        tmptabela = self.window['-TABELA-'].Values
        indice = 0
        for idx, x in enumerate(tmptabela):
            # print(x[0])
            al_ativo = aluno_inativo(x[0])
            # print(dttemp)
            if al_ativo is not None and al_ativo == 'N':
                self.window['-TABELA-'].Update(
                    row_colors=[[indice, sg.user_settings_get_entry('-coralunoinativo-')]])
                # self.window['-CAIXA-'].print(
                #    'O plano de ' + x[1] + ' tem ' + str(diasfim) + ' dias para acabar.')
                # self.planos_acabando.append((x[0], diasfim))
            indice = indice + 1

    def run(self):
        global valtmp
        while True:
            # if firstrun():
            #     self.window.write_event_value('Gráfico', '')
            #     splashscreen()
            # TESTE DO LOG DE ERROS
            # try:
            #    sprint('Vaggie')
            # except Exception as Argument:
            #    logging.error(str(Argument))

            now = datetime.now()
            now = now.strftime('%d/%m/%Y')
            if sg.user_settings_get_entry('-lastbackup-') is None:
                self.window['-STATUS-'].update('Nenhum backup efetuado.')
            else:
                ultimobkp = sg.user_settings_get_entry('-lastbackup-')
                tempobkp = diferenca_datas(ultimobkp, now)
                tmp = sg.user_settings_get_entry('-bkpperiodo-')
                tmp2 = sg.user_settings_get_entry('-bkpautomatico-')
                if int(tempobkp) >= int(tmp) and tmp2 is True:
                    tmp3 = backup_auto()
                    if tmp3 == 1:
                        sg.popup('Atenção: houve uma falha na criação do backup dos bancos de dados.')
                self.window['-STATUS-'].update('Último backup realizado há ' + str(tempobkp) + ' dias atrás.')

            if self.atrasados:
                Principal.configura_tabela(self)
                self.atrasados = False

            # tmptabela = self.window['-TABELA-'].Values
            # if self.sort:
            #     tabela_final = sort_table(tmptabela, (1,))
            #     self.window['-TABELA-'].Update(values=tabela_final)
            #     self.sort = False
            # tmptabela = self.window['-TABELA-'].Values
            # if self.atrasados:  # EDITANDO3
            #     indice = 0
            #     for idx, x in enumerate(tmptabela):
            #         atrasado = mensalidades_atraso(x[0])
            #         if atrasado:
            #             self.window['-TABELA-'].Update(
            #                 row_colors=[[indice, sg.user_settings_get_entry('-cormensatraso-')]])
            #         elif buscar_aluno_index(x[0])[10] == 'N':
            #             self.window['-TABELA-'].Update(
            #                 row_colors=[[indice, sg.user_settings_get_entry('-coralunoinativo-')]])
            #             # self.window['-CAIXA-'].print('Aluno ' + x[1] + ' em atraso.')
            #         indice = indice + 1
            #     self.atrasados = False
            # if self.planos_fim:
            #     indice = 0
            #     for idx, x in enumerate(tmptabela):
            #         # print(x[0])
            #         dttemp = planos_acabando(x[0])
            #         # print(dttemp)
            #         if dttemp is not None and dttemp != '':
            #             dtatual = datetime.strptime(dttemp, '%d/%m/%Y')
            #             dthoje = datetime.now()
            #             deltafim = dtatual - dthoje
            #             # print(deltafim.days)
            #             diasfim = int(deltafim.days)
            #             if diasfim < 30:
            #                 self.window['-TABELA-'].Update(
            #                     row_colors=[[indice, sg.user_settings_get_entry('-corplanofinal-')]])
            #                 # self.window['-CAIXA-'].print(
            #                 #    'O plano de ' + x[1] + ' tem ' + str(diasfim) + ' dias para acabar.')
            #             self.planos_acabando.append((x[0], diasfim))
            #         indice = indice + 1
            #     # print(self.planos_acabando)
            #     self.planos_fim = False

            self.event, self.values = self.window.read()
            # print(self.event,self.values)
            # if ultimobkp
            # print(self.event)
            # self.window['-TABELA-'].bind('<Enter>', '+MOUSE OVER+')
            # if (self.event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or self.event == 'Sair') and sg.popup_yes_no('Tem
            # certeza que deseja sair do programa?') == 'Yes':

            if self.event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, 'Sair', '-SAIR-'):
                opcao, _ = sg.Window('Continuar?', [[sg.T('Tem certeza que deseja sair do programa?')],
                                                    [sg.Yes(s=10, button_text='Sim'), sg.No(s=10, button_text='Não')]],
                                     disable_close=True, element_justification='center').read(close=True)
                if opcao == 'Sim':
                    sg.user_settings_set_entry('-location-', self.window.current_location())
                    break

            if self.event == 'Editar opções de treino':
                objeditaropcoes = Opcoes_treino()
                objeditaropcoes.run()

            if self.event == 'Lista de alunos(imprime)':
                pdfgen.gera_lista_pdf(alunos_nomeven())
                self.window.perform_long_operation(
                    lambda: os.system('\"' + pdfviewer + '\" ' + pdfgen.arq_lista),
                    '-FUNCTION COMPLETED-')

            if self.event == '-ADERIRPLANOS-':
                if len(self.row) != 0:
                    objadplanos = Aderir_planos()
                    objadplanos.indicealuno = self.dados[self.row[0]][0]
                    objadplanos.nomealuno = self.dados[self.row[0]][1]
                    objadplanos.run()
                else:
                    sg.Popup('Selecione um registro na tabela.')

            if self.event == 'Configurações':
                objconf = Configuracoes()
                objconf.run()

            if self.event == 'Gráfico':
                objgrafico = grafico_mensal()
                objgrafico.run()

            if self.event == 'Editar planos':
                objedplanos = Editar_planos()
                objedplanos.run()

            if self.event == 'Lembretes':
                objlembrete = Lembretes()
                objlembrete.run()

            if self.event == 'Sobre...':
                objsobre = Sobre()
                objsobre.run()

            # ################################################################
            # Janela pausa : por enquanto não implementada.
            # ################################################################

            if self.event == '-PAUSA-':
                if len(self.row) != 0:
                    self.indicep = self.dados[self.row[0]][0]
                    self.layoutp = [
                        [sg.Text('Pausa', font='_ 25')],
                        [sg.HorizontalSeparator(k='-SEP-')],
                        [sg.T('Aluno:', s=(6, 1)), sg.I(self.dados[self.row[0]][1], s=(48, 1), disabled=True)],
                        [sg.T('Plano:', k='-LBPL-', s=(6, 1), visible=False),
                         sg.I('Nenhum', k='-PLANO-', s=(25, 1), disabled=True, visible=False)],
                        [sg.pin(sg.T('Início:', k='-LBIN-', s=(6, 1), visible=False)),
                         sg.pin(sg.I(k='-INICIO-', s=(10, 1), disabled=True, visible=False)), sg.Push(),
                         sg.pin(sg.T('Fim:', k='-LBFI-', s=(6, 1), visible=False)),
                         sg.pin(sg.I(k='-FIM-', s=(10, 1), disabled=True, visible=False))],
                        [sg.T('Última mens. paga:', s=(16, 1)), sg.I(k='-ULTIMAM-', s=(10, 1), disabled=True)],
                        [sg.HorizontalSeparator(k='-SEP-')],
                        [sg.T('Início da pausa:', s=(12, 1)),
                         sg.I(datetime.strftime(datetime.now(), '%d/%m/%Y'), k='-DATA-', s=(10, 1), focus=True),
                         sg.CalendarButton('Data', locale='pt_BR', format='%d/%m/%Y',
                                           month_names=meses, day_abbreviations=dias), sg.Push(),
                         sg.T('Dias em pausa:', s=(12, 1)), sg.I(k='-PERIODO-', s=(8, 1), enable_events=True)],
                        [sg.T('Termina em:', s=(12, 1)), sg.I(k='-FIMPAUSA-', s=(10, 1)), sg.Push(),
                         sg.T('Próxima cobrança:', s=(15, 1)), sg.I(k='-PROXCOB-', s=(10, 1))],
                        [sg.HorizontalSeparator(k='-SEP-')],
                        [sg.Push(), sg.B('Confirma', k='-CONF-'), sg.B('Sair', k='-SAIR-')]
                    ]
                    self.windowp = sg.Window('Pausa', self.layoutp, finalize=True)
                    while True:
                        planos = planos_busca(self.indicep)
                        # print(planos)
                        if planos[0] is not None and planos[0] != '':
                            # print('entrou no if')
                            self.windowp['-LBPL-'].update(visible=True)
                            self.windowp['-PLANO-'].update(visible=True)
                            self.windowp['-LBIN-'].update(visible=True)
                            self.windowp['-INICIO-'].update(visible=True)
                            self.windowp['-LBFI-'].update(visible=True)
                            self.windowp['-FIM-'].update(visible=True)
                            periodo = ''
                            self.windowp['-PLANO-'].update(planos[1])
                            self.windowp['-INICIO-'].update(planos[2])
                            self.windowp['-FIM-'].update(planos[3])
                            plan = planos_ler()
                            per = 0
                            for idx, x in enumerate(plan):
                                if x[0] == planos[0]:
                                    per = x[2]
                            self.periodo = per

                        # busca a ultima mensalidade paga

                        self.eventp, self.valuesp = self.windowp.read()
                        # print(self.event3)
                        # print(self.values3)
                        if self.eventp in (None, '-SAIR-'):
                            break

                        if self.eventp == '-PERIODO-':
                            datastr = self.valuesp['-DATA-'].rstrip()
                            dtinicio = datetime.strptime(datastr, '%d/%m/%Y')
                            if self.valuesp['-PERIODO-'].rstrip() != '':
                                per = int(self.valuesp['-PERIODO-'].rstrip())
                                dtfinal = dtinicio + relativedelta(days=+per)
                                dtfinalstr = datetime.strftime(dtfinal, '%d/%m/%Y')
                                self.windowp['-FIMPAUSA-'].update(dtfinalstr)

                    self.windowp.close()
                else:
                    sg.Popup('Selecione um registro na tabela.')

            # ################################################################
            # FIM Janela pausa
            # ################################################################

            if self.event == 'Financeiro':
                objcontabil = contabil.Contabil()
                objcontabil.run()

            #                self.window.perform_long_operation(lambda: subprocess.call("contabil.exe", shell=True),
            #                                                   '-FUNCTION COMPLETED-')

            if self.event == 'Limpar banco de dados':
                opcao, _ = sg.Window('Continuar?', [[sg.T('Tem certeza?')],
                                                    [sg.Yes(s=10, button_text='Sim'), sg.No(s=10, button_text='Não')]],
                                     disable_close=True, element_justification='center').read(close=True)
                if opcao == 'Sim':
                    novobanco()
            # #################################### JANELA DE TEMAS
            if self.event == 'Mudar tema':
                self.layout3 = [[sg.Text('Navegador de temas')],
                                [sg.Text('Clique em um tema para ver uma janela de preview.')],
                                [sg.T('O tema original é DarkBlue3.')],
                                [sg.T('O novo tema será aplicado assim que você abrir o programa novamente.')],
                                [sg.Listbox(values=self.lista_temas,
                                            size=(20, 12), key='-LISTA-', enable_events=True)],
                                [sg.B('Salvar tema', k='-SALVA-'), sg.Button('Sair', k='-SAIR-')]]
                self.window3 = sg.Window('Navegador de temas', self.layout3)

                while True:
                    self.event3, self.values3 = self.window3.read()
                    # print(self.event3)
                    # print(self.values3)
                    if self.event3 in (None, '-SAIR-'):
                        break
                    sg.change_look_and_feel(self.values3['-LISTA-'][0])
                    sg.popup_get_text('Este é o tema {}'.format(self.values3['-LISTA-'][0]))

                    if self.event3 in '-SALVA-':
                        sg.user_settings_set_entry('-tema-', self.values3['-LISTA-'][0])
                        # sg.popup(self.values3['-LISTA-'][0])
                        # sg.popup(sg.user_settings_get_entry('-tema-'))
                        break
                self.window3.close()
            # #################################### JANELA DE TEMAS

            # #############################
            # RECEBE VENDA
            # #############################

            if self.event in ('-RECVENDA-', 'Receber venda'):
                if len(self.row) != 0:
                    self.indiceven = self.dados[self.row[0]][0]
                    tempvenda = venda_busca(self.indiceven)
                    naopago = False
                    for idx, x in enumerate(tempvenda):
                        if x[6] == 'NAO':
                            naopago = True
                    if naopago:
                        tmpvendas = venda_busca(self.indiceven)
                        self.layoutven = [
                            [sg.Text('Recebimento de vendas', font='_ 25')],
                            [sg.HorizontalSeparator(k='-SEP-')],
                            [sg.Text('Vendas registradas')],
                            [sg.Table(values=[],
                                      visible_column_map=[False, True, True, True],
                                      headings=self.tblhdven, max_col_width=25,
                                      auto_size_columns=False,
                                      col_widths=self.lcven,
                                      justification='left',
                                      num_rows=5,
                                      # alternating_row_color='lightblue4',
                                      key='-TABELAVEN-',
                                      # selected_row_colors='black on lightblue1',
                                      enable_events=True,
                                      expand_x=True,
                                      expand_y=True,
                                      # enable_click_events=True,
                                      # right_click_menu=self.right_click_menu,
                                      # ESTE PARAMETRO CONTROLA O MENU DO BOTAO DIREITO
                                      # select_mode=TABLE_SELECT_MODE_BROWSE,
                                      bind_return_key=True  # ESTE PARAMETRO PERMITE A LEITURA DO CLIQUE DUPLO
                                      )],
                            [sg.Push(), sg.T('Valor total: '), sg.I(size=(10, 1), k='-TOTALVEN-')],
                            [sg.Push(), sg.Button('Recebe', k='-RECEBEVEN-'),
                             sg.Button('Imprime recibo', k='-IMPRIME-', disabled=True), sg.Button('Sair', k='-SAIR-')]
                        ]
                        self.windowven = sg.Window('Receber vendas', layout=self.layoutven, finalize=True)

                        while True:
                            if not self.windowven['-TABELAVEN-'].Values:
                                print('entrou no ifnot da tabela')
                                vendastbl = []
                                self.vendasrcb = []
                                self.vlrtotal = 0.0
                                for idx, x in enumerate(tmpvendas):
                                    if x[6] == 'NAO':
                                        vendastbl.append([x[0], x[1], x[2], locale.currency(float(x[3]))])
                                        self.vendasrcb.append([x[1], x[2], locale.currency(float(x[3]))])
                                        self.vlrtotal = self.vlrtotal + float(x[3])
                                        self.tmpdata.append(x[1])
                                self.windowven['-TABELAVEN-'].update(values=vendastbl)
                                self.windowven['-TOTALVEN-'].update(locale.currency(self.vlrtotal))
                            self.eventven, self.valuesven = self.windowven.read()
                            # print(self.eventven, self.valuesven)

                            if self.eventven == '-RECEBEVEN-':
                                for idx, x in enumerate(self.tmpdata):
                                    venda_recebe(self.indiceven, x)
                                sg.Popup('Recebido com sucesso!')
                                self.windowven['-IMPRIME-'].update(disabled=False)

                            if self.eventven == '-IMPRIME-':
                                pdfgen.recibo_vendas_pdf(self.dados[self.row[0]][1],
                                                         str(locale.currency(self.vlrtotal)),
                                                         datetime.strftime(datetime.now(), '%d/%m/%Y'),
                                                         self.vendasrcb, 'Andréia')
                                self.windowven.perform_long_operation(
                                    lambda: os.system('\"' + pdfviewer + '\" ' + pdfgen.arq_recibo_vendas),
                                    '-FUNCTION COMPLETED-')

                            if self.eventven in (None, '-SAIR-'):
                                break

                        self.windowven.close()
                    else:
                        sg.popup('Não há registro de vendas para este aluno.')
                else:
                    sg.popup('Selecione um registro na tabela.')
            ##################################################
            #             JANELA VENDAS
            #
            ##################################################
            if self.event in '-VENDA-':
                if len(self.row) != 0:
                    self.indicev = self.dados[self.row[0]][0]
                    index = 0
                    tblheader = ['Indice', 'Data', 'Descrição', 'Valor']
                    largcol = [0, 12, 25, 12]
                    tmptable = []
                    valorestabela = []
                    subtotal = 0.0

                    self.framelayout = [
                        [sg.T('Aluno:', s=(6, 1)),
                         sg.I(default_text=str(buscar_aluno_index(self.indicev)[1]), k='-NOMEV-', s=(28, 1)),
                         sg.Push(), sg.T('Data:', s=(6, 1)),
                         sg.I(default_text=datetime.strftime(datetime.now(), '%d/%m/%Y'), k='-DATAV-', s=(10, 1)),
                         sg.CalendarButton('Data', locale='pt_BR', format='%d/%m/%Y',
                                           month_names=meses, day_abbreviations=dias)],
                        [sg.T('Produto:', s=(6, 1)), sg.Combo([], k='-VDESC-', s=(28, 1)), sg.Push(),
                         sg.T('Valor:', s=(6, 1)), sg.I(k='-VALORV-', s=(10, 1))],
                        [sg.Push(), sg.Button('Adiciona', k='-ADD-'), sg.Push()],
                        [sg.HorizontalSeparator(k='-SEP1-')],
                        [sg.Table(values=[],
                                  visible_column_map=[False, True, True, True],
                                  headings=tblheader, max_col_width=25,
                                  auto_size_columns=False,
                                  col_widths=largcol,
                                  justification='left',
                                  num_rows=5,
                                  # alternating_row_color='lightblue4',
                                  key='-TABELAV-',
                                  # selected_row_colors='black on lightblue1',
                                  enable_events=True,
                                  expand_x=True,
                                  expand_y=True,
                                  # enable_click_events=True, right_click_menu=self.right_click_menu, ESTE PARAMETRO
                                  # CONTROLA O MENU DO BOTAO DIREITO select_mode=TABLE_SELECT_MODE_BROWSE,
                                  bind_return_key=True  # ESTE PARAMETRO PERMITE A LEITURA DO CLIQUE DUPLO
                                  )],
                        [sg.B('Apaga', k='-VAPA-'), sg.Push(), sg.T('Valor total:'), sg.I(k='-VTOTAL-', s=(10, 1))],
                        [sg.Text('Forma de pagamento:'),
                         sg.Radio('Dinheiro', group_id='-RADIO1-', k='-RDIN-', default=True),
                         sg.Radio('Cartão', group_id='-RADIO1-', k='-RCAR-', default=False),
                         sg.Radio('Outros', group_id='-RADIO1-', k='-ROUT-', default=False)],
                        [sg.Frame('Atenção:', [[sg.Checkbox('Cobrar junto à mensalidade?',
                                                            k='-COBRA-', default=True, enable_events=True)]],
                                  background_color='Red')],
                        [sg.Push(), sg.B('Gravar/Receber', k='-GRAVA-'),
                         sg.B('Imprime', k='-IMPRIME-', disabled=True), sg.B('Voltar', k='-VOLTAR-')]
                    ]
                    self.layoutv = [
                        [sg.Image(source=icones[6]),
                         sg.Text('Venda de produtos', font='_ 25', key='-VTITLE-')],
                        [sg.HorizontalSeparator(k='-SEP-')],
                        [sg.Frame(title='', layout=self.framelayout)]
                    ]
                    self.windowv = sg.Window('Venda de produtos', self.layoutv, use_default_focus=True,
                                             finalize=True,
                                             modal=True)
                    while True:
                        self.eventv, self.valuesv = self.windowv.read()
                        if self.eventv in (sg.WIN_CLOSED, '-VOLTAR-'):
                            break
                        print(self.eventv, self.valuesv)

                        if self.eventv == '-TABELAV-':
                            self.rowv = self.valuesv[self.eventv]
                            self.dadosv = self.windowv['-TABELAV-'].Values
                            # print('ROWV', self.rowv)
                            # print('DADOSV', self.dadosv)

                        if self.eventv == '-ADD-':
                            # print(self.valuesv['-DATAV-'].rstrip())
                            # print(self.valuesv['-VDESC-'].rstrip())
                            # print(self.valuesv['-VALORV-'].rstrip())
                            tmpvar = ['', self.valuesv['-DATAV-'].rstrip(),
                                      self.valuesv['-VDESC-'].rstrip(), self.valuesv['-VALORV-'].rstrip()]
                            tmptable.append(tmpvar)
                            self.windowv['-TABELAV-'].update(values=tmptable)
                            valorestabela = self.windowv['-TABELAV-'].Values
                            subtotal = 0.0
                            for idx, x in enumerate(valorestabela):
                                subtotal = subtotal + locale.atof(x[3])
                            self.windowv['-VTOTAL-'].update(value=locale.currency(subtotal))

                        if self.eventv == '-VAPA-':
                            if len(self.rowv) != 0:
                                self.indicevv = self.dadosv[self.rowv[0]][0]
                                self.remover = self.dadosv[self.rowv[0]]
                                # self.indicev = self.rowv
                                valorestabela = self.windowv['-TABELAV-'].Values
                                # self.indicev = self.dadosv[self.rowv[0]][0]
                                # print('GET tabela', self.windowv['-TABELAV-'].get())
                                print('INDICEVV ', self.indicevv)
                                print('valorestabela ', valorestabela)
                                valorestabela.remove(self.remover)
                                # self.windowv['-TABELAV-'].update()
                                self.windowv['-TABELAV-'].update(values=valorestabela)
                                subtotal = 0.0
                                for idx, x in enumerate(valorestabela):
                                    subtotal = subtotal + locale.atof(x[3])
                                self.windowv['-VTOTAL-'].update(value=locale.currency(subtotal))
                            else:
                                sg.popup('Selecione um registro na tabela.')

                        if self.eventv == '-GRAVA-':
                            valorestabela = self.windowv['-TABELAV-'].Values
                            tmpcobranca = ''
                            tmpforma = ''
                            tmppago = ''
                            if self.valuesv['-COBRA-']:
                                tmpcobranca = 'SIM'
                            else:
                                tmpcobranca = 'NAO'
                            if self.valuesv['-RDIN-']:
                                tmpforma = 'DINHEIRO'
                            if self.valuesv['-RCAR-']:
                                tmpforma = 'CARTAO'
                            if self.valuesv['-ROUT-']:
                                tmpforma = 'OUTROS'
                            if tmpcobranca == 'SIM':
                                tmppago = 'NAO'
                            else:
                                tmppago = 'SIM'
                                self.windowv['-IMPRIME-'].update(disabled=False)
                            tmprecibo = []
                            for idx, x in enumerate(valorestabela):
                                valorstr = x[3].replace(',', '.')
                                venda_adiciona(self.indicev, x[1], x[2], valorstr, tmpcobranca, tmpforma, tmppago)
                                self.tmprecibo.append([x[1], x[2], x[3]])
                            sg.popup('Venda realizada com sucesso.')
                            # self.valuesv['-DATAV-'].rstrip()

                        if self.eventv == '-IMPRIME-':
                            pdfgen.recibo_vendas_pdf(str(buscar_aluno_index(self.indicev)[1]),
                                                     locale.currency(subtotal),
                                                     datetime.strftime(datetime.now(), '%d/%m/%Y'),
                                                     self.tmprecibo, 'Andréia')
                            self.windowv.perform_long_operation(
                                lambda: os.system('\"' + pdfviewer + '\" ' + pdfgen.arq_recibo_vendas),
                                '-FUNCTION COMPLETED-')
                    self.windowv.close()
                else:
                    sg.Popup('Selecione um registro na tabela.')

            ##################################################
            #             JANELA MAIS INFORMACOES
            ##################################################
            #
            if self.event in ('-MAISINFO-', 'Informações do aluno'):
                if len(self.row) != 0:
                    primeiro = True
                    altera_desconto = False
                    #    print('DADOS[ROW]:',dados[row[0]])
                    #    print('ROW INDEX:',dados[row[0]][0])
                    # ObjMaisInfo = MaisInfo()
                    self.indiceinfo = self.dados[self.row[0]][0]
                    # ObjMaisInfo.run()
                    self.layoutinfo = [
                        [sg.Image(source=icones[7]),
                         sg.Text('nome', font='_ 25', key='-NOMEALUNO-')],
                        [sg.HorizontalSeparator(k='-SEP-')],
                        # [sg.Text('nome',relief='sunken', font=('italic'),key='-NOMEALUNO-')],
                        # [sg.Text('Informações detalhadas')],
                        [
                            sg.TabGroup([[sg.Tab(
                                'Detalhes',
                                [
                                    # [sg.Text('', size=(7, 1))],
                                    [sg.Text('',
                                             text_color='Red', font='_ 10 bold', k='-ATRASO-')],
                                    [sg.Text('Nome:', size=(8, 1)), sg.Input(key='-NOME-', size=(41, 1))],
                                    [sg.Text('Endereço:', size=(8, 1)),
                                     sg.Input(key='-END-', size=(41, 1))],
                                    [sg.Text('Telefone:', size=(8, 1)),
                                     sg.Input(key='-TEL1-', size=(14, 1)), sg.Text('CPF:', size=(8, 1)),
                                     sg.Input(key='-CPF-', size=(14, 1))],
                                    [sg.Text('Email:', size=(8, 1)), sg.Input(key='-EMAIL-', size=(41, 1))],
                                    [sg.Text('Matrícula:', size=(8, 1)),
                                     sg.Input(key='-MAT-', size=(10, 1)),
                                     sg.CalendarButton('Data', locale='pt_BR', format='%d/%m/%Y',
                                                       month_names=meses, day_abbreviations=dias),
                                     sg.Text('Vencimento:', size=(10, 1)),
                                     sg.Input(key='-VEN-', size=(9, 1))],
                                    [sg.T('Treino:', size=(8, 1)),
                                     sg.Combo(opcao_ler_desc(), k='-OPDESC-', s=(30, 1), enable_events=True),
                                     # sg.T(''),
                                     sg.I(k='-DIAS-', s=(2, 1)), sg.T('dias', size=(3, 1))],
                                    [sg.Text('Valor mensalidade:', size=(14, 1)),
                                     sg.Input(k='-VALMENS-', size=(8, 1)), sg.Text('', size=(5, 1)),
                                     sg.Checkbox('Desconto família', k='-DESC-', enable_events=True)],
                                    [sg.Text('Data do último pagamento:'),
                                     sg.I(k='-ULTPGT-', s=(9, 1), disabled=True),
                                     sg.Text('', size=(15, 1))],
                                    [sg.Radio('Ativo', "RadioAtivo", default=True, k='-RATV-'),
                                     sg.Radio('Inativo', "RadioAtivo", k='-RINT-')],
                                    [sg.Text('', size=(1, 1))],
                                    # [sg.Button('Receber mensalidade',k='-RECEBE-')],
                                    [sg.Button('Alterar dados', k='-ALTERA-'),
                                     sg.Button('Apagar registro', k='-APAGA-')]
                                ],
                                element_justification='center', key='-mykey-',
                                expand_x=True, expand_y=True
                            ),  # expand_x=True, expand_y=True,
                                sg.Tab('Planos',
                                       [
                                           [sg.Frame('', layout=[
                                               [sg.T('Inscrito:', s=(6, 1)),
                                                sg.I('Nenhum', s=(35, 1), k='-INSCRITO-', disabled=True),
                                                sg.T('Período:', s=(6, 1)),
                                                sg.I(k='-PERIODO-', s=(15, 1), disabled=True)],
                                               [sg.T('Início:', s=(6, 1)),
                                                sg.I(k='-INICIO-', s=(15, 1), disabled=True), sg.Push(),
                                                sg.T('Final:', s=(6, 1)),
                                                sg.I(k='-FINAL-', s=(15, 1), disabled=True)],
                                           ])]
                                       ]
                                       ),
                                sg.Tab('Mensalidades',
                                       [
                                           # [sg.Text('Mensalidades')], # EDITANDO OOOOOooooOOOO
                                           [sg.Table(values=mensalidades_historico(self.indiceinfo),  # EDITANDO3
                                                     headings=self.tblheadinfo,
                                                     visible_column_map=[False, True, True, True],
                                                     # sg.Table(values=busca_dadosinfo_financeiros(self.indiceinfo),headings=self.tblheadinfo,
                                                     key='-TABELAPG-',
                                                     # max_col_width=10,
                                                     auto_size_columns=False,
                                                     col_widths=self.largcolinfo,
                                                     # pad=(5,5,5,5),
                                                     num_rows=18,
                                                     # def_col_width=5,
                                                     # alternating_row_color='lightblue4',
                                                     # selected_row_colors='black on lightblue1',
                                                     enable_events=True,
                                                     expand_x=False,
                                                     expand_y=True,
                                                     # select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                                                     # enable_click_events=True
                                                     )],
                                           # [sg.Input(key='-in2-')]
                                           [sg.Button('Apagar', k='-APAGAR-'),
                                            sg.Button('Imprime recibo', k='-IMPRIME-', focus=True)]
                                           # sg.Button('Popular tabela',k='-POP-'),
                                       ], element_justification='center', key='-mykey2-',
                                       expand_x=True, expand_y=True
                                       )
                            ]
                            ], s=(500, 350), key='-group2-', tab_location='topleft',
                                enable_events=True)], [sg.Push(), sg.Button('Voltar', k='-VOLTAR-')]
                    ]
                    self.windowinfo = sg.Window('Detalhes do aluno', self.layoutinfo, use_default_focus=True,
                                                finalize=True,
                                                modal=True)
                    # default_element_size=(12, 1),resizable=True,disable_minimize=True,
                    self.windowinfo.bind('<F1>', '-AJUDA-')
                    while True:
                        if primeiro:
                            self.windowinfo['-NOMEALUNO-'].update(str(buscar_aluno_index(self.indiceinfo)[1]))
                            self.windowinfo['-NOME-'].update(str(buscar_aluno_index(self.indiceinfo)[1]))
                            self.windowinfo['-END-'].update(str(buscar_aluno_index(self.indiceinfo)[2]))
                            self.windowinfo['-TEL1-'].update(str(buscar_aluno_index(self.indiceinfo)[3]))
                            self.windowinfo['-CPF-'].update(str(buscar_aluno_index(self.indiceinfo)[4]))
                            self.windowinfo['-EMAIL-'].update(str(buscar_aluno_index(self.indiceinfo)[5]))
                            self.windowinfo['-MAT-'].update(str(buscar_aluno_index(self.indiceinfo)[6]))
                            self.windowinfo['-VEN-'].update(str(buscar_aluno_index(self.indiceinfo)[7]))
                            self.windowinfo['-VALMENS-'].update(str(buscar_aluno_index(self.indiceinfo)[8]))
                            self.windowinfo['-ULTPGT-'].update(str(buscar_aluno_index(self.indiceinfo)[9]))
                            self.windowinfo['-OPDESC-'].update(buscar_aluno_index(self.indiceinfo)[11])
                            self.windowinfo['-DIAS-'].update(buscar_aluno_index(self.indiceinfo)[12])
                            desctmp = buscar_aluno_index(self.indiceinfo)[13]
                            if desctmp != 0.0 and desctmp is not None:
                                self.windowinfo['-DESC-'].update(value=True)

                            planos = planos_busca(self.indiceinfo)
                            # print(planos)
                            if planos[0] is not None and planos[0] != '':
                                if self.planoinfo:
                                    # print('entrou no if')
                                    periodo = ''
                                    self.windowinfo['-INSCRITO-'].update(planos[1])
                                    plan = planos_ler()
                                    for idx, x in enumerate(plan):
                                        if x[0] == planos[0]:
                                            periodo = x[2]
                                    self.windowinfo['-PERIODO-'].update(str(periodo) + ' meses')
                                    self.windowinfo['-INICIO-'].update(planos[2])
                                    self.windowinfo['-FINAL-'].update(planos[3])
                                    # self.windowinfo['-VALOR-'].update(planos[2])
                                    self.planoinfo = False

                            if buscar_aluno_index(self.indiceinfo)[10] == 'S':
                                self.windowinfo['-RATV-'].update(value=True)
                            else:
                                self.windowinfo['-RINT-'].update(value=True)
                            # Em atraso -- falta elaborar
                            # datastr = str(buscar_aluno_index(self.indiceinfo)[7]) + '/' + \
                            #          datetime.strftime(datetime.now(), '%m/%Y')
                            # datavenc = datetime.strptime(datastr, '%d/%m/%Y')
                            # if datavenc < datetime.now():
                            #    atraso = datetime.now() - datavenc
                            #    atrasostr = atraso.days
                            #    scrstr = 'Mensalidade em atraso: ' + str(atrasostr) + ' dias.'
                            #    self.windowinfo['-ATRASO-'].update(scrstr)
                            atraso = mensalidades_atraso(self.indiceinfo)
                            if atraso:
                                scrstr = 'Mensalidades em atraso: '
                                scrstr2 = ''
                                for idx, x in enumerate(atraso):
                                    scrstr2 = scrstr2 + ' ' + x
                                scrstr = scrstr + scrstr2
                                self.windowinfo['-ATRASO-'].update(scrstr)
                            primeiro = False
                        #########################
                        self.eventinfo, self.valuesinfo = self.windowinfo.read()
                        if self.eventinfo == sg.WIN_CLOSED or self.eventinfo == '-VOLTAR-':
                            break

                        if self.eventinfo == '-DESC-':
                            desc_tmp = buscar_aluno_index(self.indiceinfo)[13]
                            if ((desc_tmp is None) or (desc_tmp == 0.0)) \
                                    and self.valuesinfo['-DESC-']:
                                altera_desconto = True
                                print('desctmp = 0 and DESC true')
                            elif (desc_tmp != 0.0 and desc_tmp is not None) and not self.valuesinfo['-DESC-']:
                                altera_desconto = True
                                print('desctmp = 1 and not DESC')
                            else:
                                altera_desconto = False
                                print('else')

                        if self.eventinfo == '-TABELAPL-':
                            self.rowinfop = self.valuesinfo[self.eventinfo]
                            self.dadosinfop = self.windowinfo['-TABELAPL-'].Values

                        if self.eventinfo == '-AJUDA-':
                            obj_ajuda = Ajuda()
                            obj_ajuda.nomearquivo = 'informacoes.html'
                            obj_ajuda.run()

                        if self.eventinfo == '-APAGAR-':
                            if len(self.rowinfo) != 0:
                                opcao, _ = sg.Window('Continuar?',
                                                     [[sg.T('Tem certeza? Esta operação é definitiva.')],
                                                      [sg.Yes(s=10, button_text='Sim'),
                                                       sg.No(s=10, button_text='Não')]], disable_close=True,
                                                     modal=True).read(close=True)
                                if opcao == 'Sim':
                                    apaga_dados_financeiros(self.dadosinfo[self.rowinfo[0]][0],
                                                            self.dadosinfo[self.rowinfo[0]][1])
                                    # self.windowinfo['-TABELAPG-'].update(
                                    #     valuesinfo=busca_dados_financeiros(self.indiceinfo))
                                    self.windowinfo['-TABELAPG-'].update(
                                        valuesinfo=mensalidades_historico(self.indiceinfo))
                        if self.eventinfo == '-POP-' or self.eventinfo == '-group2-':
                            self.windowinfo['-TABELAPG-'].update(mensalidades_historico(self.indiceinfo))

                        ##########################################
                        # CHECAGEM DE VALORES
                        ##########################################
                        if self.eventinfo == '-ALTERA-':
                            if self.valuesinfo['-NOME-'].rstrip() == '':
                                sg.popup('Campo nome não pode ser vazio.')
                            elif self.valuesinfo['-END-'].rstrip() == '':
                                sg.popup('Campo endereço não pode ser vazio.')
                            elif self.valuesinfo['-TEL1-'].rstrip() != '' and \
                                    not re.fullmatch(regexTelefone, self.valuesinfo['-TEL1-'].rstrip()):
                                sg.popup('Telefone deve ser no formato (xx)xxxxx-xxxx')
                            # elif self.valuesinfo['-CPF-'].rstrip() != '' and not \
                            #         re.fullmatch(regexCPF, self.valuesinfo['-CPF-'].rstrip()):
                            #     sg.popup('CPF deve ser no formato 000.000.000-00')
                            elif self.valuesinfo['-CPF-'].rstrip() != '' and \
                                    not valida_cpf(self.valuesinfo['-CPF-'].rstrip()):
                                sg.popup('CPF inválido.')
                            elif self.valuesinfo['-EMAIL-'].rstrip() != '' and not \
                                    re.fullmatch(regexEmail, self.valuesinfo['-EMAIL-'].rstrip()):
                                sg.popup('Campo email deve ser no formato abc@de.fgh')
                            elif self.valuesinfo['-MAT-'].rstrip() == '':
                                sg.popup('Data de matrícula não pode ser vazio.')
                            elif self.valuesinfo['-VEN-'].rstrip() == '':
                                sg.popup('Data de vencimento não pode ser vazio.')
                            elif self.valuesinfo['-VALMENS-'].rstrip() == '':
                                sg.popup('Campo valor da mensalidade não pode ser vazio.')
                            elif self.valuesinfo['-VALMENS-'].rstrip() != '' and not \
                                    re.fullmatch(regexDinheiro, self.valuesinfo['-VALMENS-'].rstrip()):
                                sg.popup('Valor da mensalidade deve ser no formato xxx,xx')
                            elif self.valuesinfo['-VEN-'].rstrip() != '' and not \
                                    re.fullmatch(regexDia, self.valuesinfo['-VEN-'].rstrip()):
                                sg.popup('Data de vencimento deve ser entre 01 e 31.')
                            elif self.valuesinfo['-VALMENS-'].rstrip() != '' and not \
                                    re.fullmatch(regexDinheiro, self.valuesinfo['-VALMENS-'].rstrip()):
                                sg.popup('Valor da mensalidade deve ser no formato xxx,xx')
                            elif opcao_buscar_desc(self.valuesinfo['-OPDESC-']) == 0:
                                sg.popup('Opção de treino inválida. Favor selecionar das opções existentes.')
                            else:
                                ##########################################
                                # CHECAGEM DE VALORES
                                ##########################################
                                opcao, _ = sg.Window('Continuar?', [[sg.T('Aceita as alterações?')],
                                                                    [sg.Yes(s=10, button_text='Sim'),
                                                                     sg.No(s=10, button_text='Não')]],
                                                     disable_close=True, modal=True).read(close=True)
                                if opcao == 'Sim':
                                    cad_atv = ''
                                    desconto_final = buscar_aluno_index(self.indiceinfo)[13]
                                    valor_final_mensalidade = self.valuesinfo['-VALMENS-'].rstrip()
                                    if altera_desconto:
                                        altera_desconto = False
                                        opcao, _ = sg.Window('Continuar?', [[sg.T('Aplica desconto família?')],
                                                                            [sg.Yes(s=10, button_text='Sim'),
                                                                             sg.No(s=10, button_text='Não')]],
                                                             disable_close=True, modal=True).read(close=True)
                                        if opcao == 'Sim':
                                            print(self.valuesinfo['-DESC-'])
                                            desconto_original = buscar_aluno_index(self.indiceinfo)[13]
                                            print(desconto_original)
                                            valor_mens_str = self.valuesinfo['-VALMENS-'].rstrip()
                                            valor_mens_str = valor_mens_str.replace(',', '.')
                                            valor_mens = float(valor_mens_str)
                                            if (desconto_original != 0.0 and desconto_original is not None) \
                                                    and not self.valuesinfo['-DESC-']:
                                                # porc_desc = float(sg.user_settings_get_entry(
                                                # '-valordescontofamilia-')) valor_desc = valor_mens * porc_desc
                                                # valor_final = (10.0 * valor_mens) / 9 print(valor_final) print(
                                                # 'entrou desc. original 1 e not desc') print(self.valuesinfo[
                                                # '-DESC-']) print(porc_desc, valor_desc, valor_final)
                                                # valor_final_str = str(valor_final) valor_final_str =
                                                # valor_final_str.replace('.', ',') valor_final_mensalidade =
                                                # valor_final_str + '0'
                                                desconto_final = 0.0
                                            elif ((desconto_original is None) or (desconto_original == 0.0)) \
                                                    and self.valuesinfo['-DESC-']:
                                                desconto_final = \
                                                    float(sg.user_settings_get_entry('-valordescontofamilia-'))
                                                # valor_desc = valor_mens * porc_desc
                                                # valor_final = valor_mens - valor_desc
                                                # print('entrou desconto original = 0 e desc ativado')
                                                # print(porc_desc, valor_desc, valor_final)
                                                # print(self.valuesinfo['-DESC-'])
                                                # valor_final_str = str(valor_final)
                                                # valor_final_str = valor_final_str.replace('.', ',')
                                                # valor_final_mensalidade = valor_final_str + '0'
                                                # desconto_final = 1

                                    # print(self.windowinfo['-RATV-'])
                                    if self.valuesinfo['-RATV-']:
                                        cad_atv = 'S'
                                    else:
                                        cad_atv = 'N'
                                    alterar_aluno(self.valuesinfo['-NOME-'].rstrip(), self.valuesinfo['-END-'].rstrip(),
                                                  self.valuesinfo['-TEL1-'].rstrip(), self.valuesinfo['-CPF-'].rstrip(),
                                                  self.valuesinfo['-EMAIL-'].rstrip(),
                                                  self.valuesinfo['-MAT-'].rstrip(), self.valuesinfo['-VEN-'].rstrip(),
                                                  valor_final_mensalidade, cad_atv, desconto_final, self.indiceinfo)
                                    opcao_tmp = opcao_buscar_desc(self.valuesinfo['-OPDESC-'])
                                    opcao_atualiza(self.indiceinfo, opcao_tmp[0], opcao_tmp[1], opcao_tmp[2])
                                    if self.values['-BUSCAR-'] != '':
                                        if self.values['-ATIVOS-']:
                                            busca = buscar_por_nome(str(self.values['-BUSCAR-'].rstrip()), True)
                                        else:
                                            busca = buscar_por_nome(str(self.values['-BUSCAR-'].rstrip()), False)
                                        Principal.configura_tabela(self)
                                        # tabela_final = sort_table(tmptabela, (1,))
                                        # self.window['-TABELA-'].Update(values=tabela_final)
                                        # self.window['-TABELA-'].update(values=busca)
                                        # indice = 0
                                        # for idx, x in enumerate(tmptabela):
                                        #     atrasado = mensalidades_atraso(x[0])  # EDITANDO CORES DA TABELA
                                        #     if atrasado:
                                        #         self.window['-TABELA-'].Update(row_colors=[
                                        #             [indice, sg.user_settings_get_entry('-cormensatraso-')]])
                                        #         # self.window['-CAIXA-'].print('Aluno ' + x[1] + ' em atraso.')
                                        #     indice = indice + 1
                                        # indice = 0
                                        # for idx, x in enumerate(tmptabela):
                                        #     # print(x[0])
                                        #     dttemp = planos_acabando(x[0])
                                        #     # print(dttemp)
                                        #     if dttemp is not None and dttemp != '':
                                        #         dtatual = datetime.strptime(dttemp, '%d/%m/%Y')
                                        #         dthoje = datetime.now()
                                        #         deltafim = dtatual - dthoje
                                        #         # print(deltafim.days)
                                        #         diasfim = int(deltafim.days)
                                        #         if diasfim < 30:
                                        #             self.window['-TABELA-'].Update(row_colors=[
                                        #                 [indice, sg.user_settings_get_entry('-corplanofinal-')]])
                                        #         self.planos_acabando.append((x[0], diasfim))
                                        #     indice = indice + 1
                                    else:
                                        if self.values['-ATIVOS-']:
                                            temp = ler_todos_dados_ativos()
                                        else:
                                            temp = ler_todos_dados()
                                        # temp = ler_todos_dados()

                                        self.window['-TABELA-'].update(values=temp)
                                        Principal.configura_tabela(self)
                                        # # CODIGO PARA AS CORES DA TABELA
                                        # tabela_final = sort_table(tmptabela, (1,))
                                        # self.window['-TABELA-'].Update(values=tabela_final)
                                        # tmptabela = self.window['-TABELA-'].Values
                                        # indice = 0
                                        # for idx, x in enumerate(tmptabela):
                                        #     atrasado = mensalidades_atraso(x[0])
                                        #     if atrasado:
                                        #         self.window['-TABELA-'].Update(row_colors=[
                                        #             [indice, sg.user_settings_get_entry('-cormensatraso-')]])
                                        #         # self.window['-CAIXA-'].print('Aluno ' + x[1] + ' em atraso.')
                                        #     indice = indice + 1
                                        # indice = 0
                                        # for idx, x in enumerate(tmptabela):
                                        #     # print(x[0])  # EDITANDO
                                        #     dttemp = planos_acabando(x[0])
                                        #     # print(dttemp)
                                        #     if dttemp is not None and dttemp != '':
                                        #         dtatual = datetime.strptime(dttemp, '%d/%m/%Y')
                                        #         dthoje = datetime.now()
                                        #         deltafim = dtatual - dthoje
                                        #         print(deltafim.days)
                                        #         diasfim = int(deltafim.days)
                                        #         if diasfim < 30:
                                        #             self.window['-TABELA-'].Update(row_colors=[
                                        #                 [indice, sg.user_settings_get_entry('-corplanofinal-')]])
                                        #             # self.window['-CAIXA-'].print( 'O plano de ' + x[1] + ' tem ' +
                                        #             # str(diasfim) + ' dias para acabar.')
                                        #         self.planos_acabando.append((x[0], diasfim))
                                        #     indice = indice + 1
                                    sg.Popup('Alterações efetuadas com sucesso.')

                        #########################################
                        # GERA RECIBO PARA IMPRESSAO
                        #########################################

                        if self.eventinfo == '-TABELAPG-':
                            self.rowinfo = self.valuesinfo[self.eventinfo]
                            self.dadosinfo = self.windowinfo['-TABELAPG-'].Values

                        if self.eventinfo == '-IMPRIME-':
                            if len(self.rowinfo) != 0:
                                # print('Self.dadosinfo ', self.dadosinfo)
                                # print('RECIBO')
                                # print(self.valuesinfo['-NOME-'].rstrip(),self.dadosinfo[self.rowinfo[0]][2],self.dadosinfo[self.rowinfo[0]][0],self.valuesinfo['-VEN-'].rstrip(),self.dadosinfo[self.rowinfo[0]][1],self.dadosinfo[self.rowinfo[0]][3])
                                # print(self.valuesinfo['-NOME-'].rstrip(),str(self.dadosinfo[self.rowinfo[0]][2]),str(self.dadosinfo[self.rowinfo[0]][0]),self.valuesinfo['-VEN-'].rstrip(),str(self.dadosinfo[self.rowinfo[0]][1]),str(self.dadosinfo[self.rowinfo[0]][3]))
                                if str(self.dadosinfo[self.rowinfo[0]][2]) != '':
                                    pdfgen.gera_recibo_pdf(self.valuesinfo['-NOME-'].rstrip(),
                                                           str(self.dadosinfo[self.rowinfo[0]][3]),
                                                           str(self.dadosinfo[self.rowinfo[0]][2]),
                                                           self.valuesinfo['-VEN-'].rstrip(),
                                                           str(self.dadosinfo[self.rowinfo[0]][0]),
                                                           str('Andréia'))
                                    self.windowinfo.perform_long_operation(
                                        lambda: os.system('\"' + pdfviewer + '\" ' + pdfgen.arq_recibo),
                                        '-FUNCTION COMPLETED-')
                                else:
                                    sg.popup('Mensalidade em aberto.')
                            # os.system(arq_recibo)
                            #    print('dadosinfo[rowinfo]:',dadosinfo[rowinfo[0]])
                            #    print('rowinfo INDEX:',dadosinfo[rowinfo[0]][0])
                            #                    ObjMaisInfo = MaisInfo()
                            #                    ObjMaisInfo.indiceinfo = self.dadosinfo[self.rowinfo[0]][0]
                            #                    ObjMaisInfo.run()
                            else:
                                sg.Popup('Selecione um registro na tabela.')

                        if self.eventinfo == '-APAGA-':
                            opcao, _ = sg.Window('Continuar?', [[sg.T('Tem certeza? Esta operação é definitiva.')],
                                                                [sg.Yes(s=10, button_text='Sim'),
                                                                 sg.No(s=10, button_text='Não')]], disable_close=True,
                                                 modal=True).read(close=True)
                            # if opcao == 'Não':
                            #    break
                            if opcao == 'Sim':

                                apaga_registro(self.indiceinfo)
                                if self.values['-ATIVOS-']:
                                    temp = ler_todos_dados_ativos()
                                else:
                                    temp = ler_todos_dados()
                                # temp = ler_todos_dados()
                                self.window['-TABELA-'].update(values=temp)
                                sg.Popup('Registro excluído definitivamente.')
                                break
                    # print(self.eventinfo, self.valuesinfo)
                    self.windowinfo.close()

                else:
                    sg.Popup('Selecione um registro na tabela.')
            ##################################################
            #             JANELA MAIS INFORMACOES
            ##################################################

            #            if self.event == '-ATIVOS-':
            #                if self.values['-ATIVOS-']:
            #                    busca = ler_todos_dados_ativos()
            #                else:
            #                    busca = ler_todos_dados()
            # print(busca)
            #                self.window['-TABELA-'].update(values=busca)

            if self.event == 'Backup parcial':
                obj_backup_db = BackupDB()
                obj_backup_db.run()

            if self.event == 'Backup completo':
                obj_backup_completo = BackupCompleto()
                obj_backup_completo.run()

            if self.event == 'Tela principal':
                obj_ajuda = Ajuda()
                obj_ajuda.nomearquivo = 'telaprincipal.html'
                obj_ajuda.run()

            if self.event == 'Recebimento':
                obj_relatorio_mensal = RelatorioMensal()
                obj_relatorio_mensal.run()

            if self.event == 'Devedores':
                obj_rel_nao_pago = RelNaoPago()
                obj_rel_nao_pago.run()

            if self.event == '-BBUSCA-' or self.event == '-ATIVOS-':
                # print(str(self.values['-BUSCAR-'].rstrip()))
                # busca = buscar_por_nome(str(self.window['-BUSCAR-']))
                if self.values['-ATIVOS-']:
                    busca = buscar_por_nome(str(self.values['-BUSCAR-'].rstrip()), True)
                else:
                    busca = buscar_por_nome(str(self.values['-BUSCAR-'].rstrip()), False)
                # busca = buscar_por_nome(str(self.values['-BUSCAR-'].rstrip()))
                # print(busca)
                # self.atrasados = True
                # self.planos_fim = True
                # self.sort = True
                self.window['-TABELA-'].update(values=busca)
                Principal.configura_tabela(self)

            # if self.event == '-ATUALIZAR-':
            #    sg.popup_non_blocking('Popup', *self.values['-ATUALIZAR-'])

            if self.event in ('-LIMPA-', '-ATUALIZAR-'):
                # print(str(self.values['-BUSCAR-'].rstrip()))
                self.window['-BUSCAR-'].update('')
                # busca = buscar_por_nome(str(self.values['-BUSCAR-'].rstrip()))
                if self.values['-ATIVOS-']:
                    busca = ler_todos_dados_ativos()
                else:
                    busca = ler_todos_dados()
                # print(busca)
                # self.atrasados = True
                # self.planos_fim = True
                # self.sort = True
                self.window['-TABELA-'].update(values=busca)
                Principal.configura_tabela(self)

            ##################################################
            #             JANELA CADASTRO ALUNO
            ##################################################

            if self.event == '-AD-' or self.event == 'Adicionar aluno':
                self.layout2 = [
                    [sg.Image(source=icones[7]),
                     sg.Text('Cadastro', font='_ 25', key='-NOMEALUNO-')],
                    [sg.HorizontalSeparator(k='-SEP-')],
                    [sg.Text('', size=(7, 1))],
                    [sg.Text('Nome:', size=(8, 1)),
                     sg.Input(key='-NOME-', size=(41, 1), tooltip='Nome do aluno', focus=True)],
                    [sg.Text('Endereço:', size=(8, 1)), sg.Input(key='-END-', size=(41, 1), tooltip='Endereço')],
                    [sg.Text('Telefone:', size=(8, 1)),
                     sg.Input(key='-TEL1-', size=(14, 1), tooltip='Telefone ou celular'), sg.Push(),
                     sg.Text('CPF:', size=(6, 1)),
                     sg.Input(key='-CPF-', size=(14, 1), tooltip='Pode ficar em branco')],  # ,enable_events=True
                    [sg.Text('Email:', size=(8, 1)), sg.Input(key='-EMAIL-', size=(41, 1))],
                    [sg.Text('Matrícula:', size=(8, 1)),
                     sg.Input(key='-MAT-', size=(9, 1), tooltip='Data da matrícula (não pode ficar em branco)'),
                     sg.CalendarButton('Data', locale='pt_BR', format='%d/%m/%Y', month_names=meses,
                                       day_abbreviations=dias), sg.Push(),
                     sg.Text('Vencimento dia:', size=(12, 1)),
                     sg.Input(key='-VEN-', size=(6, 1), tooltip='Dia do vencimento da mensalidade com dois dígitos')],
                    [sg.T('Opção:', size=(8, 1)),
                     sg.Combo(opcao_ler_desc(), readonly=True, size=(39, 1), enable_events=True, k='-OPCAO-')],
                    [sg.Push(), sg.Text('Valor da mensalidade R$:', size=(19, 1)),
                     sg.Input(key='-VALMENS-', size=(8, 1),
                              tooltip='Valor da mensalidade no formato xxx,xx', enable_events=True)],
                    [sg.Checkbox('Desconto família (% na mensalidade)', enable_events=True, k='-DESC-')],

                    # [sg.Radio('Ativo', "RadioAtivo", default=True, k='-RATV-'), sg.Radio('Inativo', "RadioAtivo",
                    # k='-RINT-')],

                    [sg.Text('', size=(7, 1))],
                    [sg.Push(), sg.Button('Cadastrar', key='-CAD-', bind_return_key=True),
                     sg.Button('Ajuda', k='-AJUDA-'),
                     sg.Button('Fechar', key='-FECHAR-')]
                ]

                self.window2 = sg.Window('Cadastro', self.layout2, use_default_focus=True, finalize=True, modal=True)
                self.window2.bind('<F1>', '-AJUDA-')
                # desc_tmp = sg.user_settings_get_entry('-valordescontofamilia-', 0.1)
                # desc_tmp = str(round(float(desc_tmp) * 100))
                # self.window['-DESC-'].update(value='Desconto família (' + desc_tmp + '% na mensalidade')
                while True:

                    dttmp = datetime.now()
                    dttmp2 = dttmp.strftime('%d/%m/%Y')
                    self.window2['-MAT-'].update(dttmp2)
                    self.window2['-VEN-'].update('10')
                    self.event2, self.values2 = self.window2.read()
                    # print(self.event2,self.values2)
                    # print(self.event2)
                    # print(self.values2)
                    if self.event2 == sg.WIN_CLOSED or self.event2 == '-FECHAR-':
                        break

                    if self.event2 == '-OPCAO-':
                        print(self.values2['-OPCAO-'])
                        self.opcaoselec = opcao_buscar_desc(self.values2['-OPCAO-'])
                        print(self.opcaoselec)
                        print(self.opcaoselec[0])
                        print(self.opcaoselec[1])
                        print(self.opcaoselec[2])

                    if self.event2 == '-VALMENS-':
                        self.vtmp = True

                    # if self.event2 == '-DESC-':
                    #     print(self.window2['-DESC-'].get())
                    #     if self.values2['-VALMENS-'] != '':
                    #         if self.vtmp:
                    #             valtmp = self.values2['-VALMENS-']
                    #             self.vtmp = False
                    #             print(valtmp)
                    #         if self.window2['-DESC-'].get():
                    #             valtmp2 = valtmp.replace(',', '.')
                    #             desc = float(valtmp2) * 0.1
                    #             valfinal = float(valtmp2) - desc
                    #             vfinalstr = str(valfinal)
                    #             vfinalstr = vfinalstr.replace('.', ',')
                    #             vfinalstr = vfinalstr + '0'
                    #             self.window2['-VALMENS-'].update(vfinalstr)
                    #             self.desconto = True
                    #         else:
                    #             self.window2['-VALMENS-'].update(valtmp)
                    #             print(valtmp)
                    #             self.desconto = False

                    if self.event2 == '-AJUDA-':
                        obj_ajuda = Ajuda()
                        obj_ajuda.nomearquivo = 'cadastro.html'
                        obj_ajuda.run()

                    if self.event2 == '-CAD-':
                        if self.values2['-NOME-'].rstrip() == '':
                            sg.popup('Campo nome não pode ser vazio.')
                        elif self.values2['-END-'].rstrip() == '':
                            sg.popup('Campo endereço não pode ser vazio.')
                        elif self.values2['-TEL1-'].rstrip() != '' and not \
                                re.fullmatch(regexTelefone, self.values2['-TEL1-'].rstrip()):
                            sg.popup('Telefone deve ser no formato (xx)xxxxx-xxxx')
                        elif self.values2['-CPF-'].rstrip() != '' and not \
                                re.fullmatch(regexCPF, self.values2['-CPF-'].rstrip()):
                            sg.popup('CPF deve ser no formato 000.000.000-00')
                        elif self.values2['-CPF-'].rstrip() != '' and not valida_cpf(self.values2['-CPF-'].rstrip()):
                            sg.popup('CPF inválido.')
                        elif self.values2['-EMAIL-'].rstrip() != '' and not \
                                re.fullmatch(regexEmail, self.values2['-EMAIL-'].rstrip()):
                            sg.popup('Campo email deve ser no formato aaa@aaa.aaa')
                        elif self.values2['-MAT-'].rstrip() == '':
                            sg.popup('Data de matrícula não pode ser vazio.')
                        elif self.values2['-VEN-'].rstrip() == '':
                            sg.popup('Dia de vencimento não pode ser vazio.')
                        elif self.values2['-VALMENS-'].rstrip() == '':
                            sg.popup('Campo valor da mensalidade não pode ser vazio.')
                        elif self.values2['-VALMENS-'].rstrip() != '' and not \
                                re.fullmatch(regexDinheiro, self.values2['-VALMENS-'].rstrip()):
                            sg.popup('Valor da mensalidade deve ser no formato xxx,xx.')
                        elif self.values2['-VEN-'].rstrip() != '' and not \
                                re.fullmatch(regexDia, self.values2['-VEN-'].rstrip()):
                            sg.popup('Data de vencimento deve ser entre 01 e 31.')
                        elif self.values2['-VALMENS-'].rstrip() != '' and not \
                                re.fullmatch(regexDinheiro, self.values2['-VALMENS-'].rstrip()):
                            sg.popup('Valor da mensalidade deve ser no formato xxx,xx')
                        elif self.values2['-OPCAO-'] == '':
                            sg.popup('Selecione uma opção de treino.')
                        else:
                            # cad_atv = ''
                            # if self.values['-RATV-']:
                            #    cad_atv='S'
                            # else:
                            #    cad_atv='N'
                            if self.values2['-DESC-']:  # EDITANDO2
                                tmpdesc = float(sg.user_settings_get_entry('-valordescontofamilia-'))
                            else:
                                tmpdesc = 0.0
                            cadastrar_aluno(self.values2['-NOME-'].rstrip(), self.values2['-END-'].rstrip(),
                                            self.values2['-TEL1-'].rstrip(), self.values2['-CPF-'].rstrip(),
                                            self.values2['-EMAIL-'].rstrip(), self.values2['-MAT-'].rstrip(),
                                            self.values2['-VEN-'].rstrip(), self.values2['-VALMENS-'].rstrip(), 'S',
                                            self.opcaoselec[0], self.opcaoselec[1], self.opcaoselec[2], tmpdesc)
                            # cria uma entrada para este aluno no banco mensalidades
                            mensalidades_cria_tabela(alunos_ultimo())
                            self.window2['-NOME-'].update('')
                            self.window2['-END-'].update('')
                            self.window2['-TEL1-'].update('')
                            self.window2['-CPF-'].update('')
                            self.window2['-EMAIL-'].update('')
                            self.window2['-MAT-'].update('')
                            self.window2['-VEN-'].update('')
                            self.window2['-VALMENS-'].update('')
                            self.window2['-NOME-'].SetFocus()
                            # sg.popup('Cadastro realizado com sucesso.')
                            self.cad_real = True
                            if self.values['-ATIVOS-']:
                                temp = ler_todos_dados_ativos()
                            else:
                                temp = ler_todos_dados()
                            # temp = ler_todos_dados()
                            # self.atrasados = True
                            # self.planos_fim = True
                            self.window['-TABELA-'].update(values=temp)
                            Principal.configura_tabela(self)
                self.window2.close()

            ##################################################
            #             JANELA CADASTRO ALUNO
            ##################################################

            if self.event == '-TABELA-':
                # if self.event == 'bind_return_key':
                self.row = self.values[self.event]
                self.dados = self.window['-TABELA-'].Values
                # print(self.row)
                # print(self.dados)
                # aluno = buscar_aluno_index(indice)
                # indice = ler_todos_dados()[row]
                # i = 0
                # while i < len(row):
                #    print('DT_SEL', row[i])
                #    i = i + 1
                # print('ROW',row)

            if self.event in ('-RECEBE-', 'Receber mensalidade'):
                if len(self.row) != 0:
                    # if mensalidade_busca(self.dados[self.row[0]][0]):
                    #     print(str(mensalidade_busca(self.dados[self.row[0]][0])))
                    #     tmpstring = str(mensalidade_busca(self.dados[self.row[0]][0]))
                    #     finalstr = tmpstring.translate({ord(c): None for c in "[(',)]"})
                    #     print('finalstr: ', finalstr)
                    #     print('numero aluno: ', self.dados[self.row[0]][0])
                    #     tmpdate = datetime.strptime(finalstr, '%d/%m/%Y')
                    #     print(tmpdate)
                    #     # tmpdate = tmpdate[3:5]
                    #     tmpnowstr = datetime.strftime(datetime.now(), '%d/%m/%Y')
                    #     tmpnow = datetime.strptime(tmpnowstr, '%d/%m/%Y')
                    #     # tmpnow = tmpnow[0:2]
                    #     if tmpdate < tmpnow:
                    #         obj_recebe = Pagamentos()
                    #         obj_recebe.indicealuno = self.dados[self.row[0]][0]
                    #         obj_recebe.nomealuno = self.dados[self.row[0]][1]
                    #         obj_recebe.run()
                    #     else:
                    #         sg.popup('Este aluno já pagou a mensalidade deste mês.')
                    # else:
                    obj_recebe = Pagamentos()
                    obj_recebe.indicealuno = self.dados[self.row[0]][0]
                    obj_recebe.nomealuno = self.dados[self.row[0]][1]
                    obj_recebe.run()
                else:
                    sg.Popup('Selecione um registro na tabela.')
                # row =
                # if len(row) != 0:
                # ObjRecebe = Recebe()
                # ObjRecebe.indicealuno = dados
                # ObjRecebe.run()

                # data_selected =
                # data_selected = [ler_todos_dados()[row] for row in self.values[self.event]]
                # print('ROW:',row)
                # print('LEN ROW:',len(row))
                # if len(row) == 0:
                #   print('SAINDO DO CODIGO')
                # else:
                # data_selected = [ler_todos_dados()[row] for row in self.values[self.event]]
                # print(row)
                # i = 0
                # while i < len(data_selected[0]):
                #    print('DT_SEL', data_selected[0][i])
                #    i = i + 1
                # print('DataSelected:', data_selected[0][0])
                # data_index=int(data_selected[0][0])
                # print('indice:', data_index)
                #    ObjMaisInfo = MaisInfo()
                # ObjMaisInfo.indice = data_index
                # print('ObjMaisInfo.indice',ObjMaisInfo.indice)
                #   ObjMaisInfo.run() #PAREI AQUIs
                # print(row)
                # if row:
                # sg.Popup(f'Selected row is {row}')
                # dados_aluno = str(indice_aluno(self.values['listagem'][0]))
                # ObjMaisInfo = MaisInfo()
                # ObjMaisInfo.indice = dados_aluno
                # ObjMaisInfo.run()
            # if isinstance(self.event, tuple):
            #    if self.event[0] == '-TABLE-':

            # if self.event[2][0] == -1 and self.event[2][1] != -1:           # Header was clicked and wasn't the
            # "row" column

            #            col_num_clicked = self.event[2][1]
            #        self.window['-CLICKED-'].update(f'{self.event[2][0]},{self.event[2][1]}')
            # if self.event == '-TABELA-':
            #    print('EVENTO TABELA!')
            # print(self.values)
            # print(self.event)
        self.window.close()


# FINAL TELA PRINCIPAL

# INICIO TELA DE BACKUP
class BackupDB:
    pastabkp = ''
    endereco = os.getcwd()
    nomearq = ''
    nomedapasta = 'db'
    enderecopai = os.path.dirname(endereco)

    def __init__(self):
        self.values = None
        self.event = None
        self.layout = [
            [sg.Image(source=icones[1]),
             sg.Text('Cópia de segurança', font='_ 25')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.Text('Selecione a pasta onde deseja guardar uma cópia dos bancos de dados:')],
            [sg.Combo(sorted(sg.user_settings_get_entry('-foldernames-', [])),
                      default_value=sg.user_settings_get_entry('-last foldername-', ''), size=(50, 1),
                      key='-FOLDERNAME-'), sg.FolderBrowse('Abrir pasta...')],
            [sg.Button('Gerar cópia', k='-BACKUP-'), sg.Button('Sair', k='-SAIR-')]
        ]

        self.window = sg.Window('Cópia de segurança', self.layout, )

    def run(self):
        while True:
            self.event, self.values = self.window.read()
            if self.event in (sg.WIN_CLOSED, '-SAIR-'):
                break
            if self.event == '-BACKUP-':
                sg.user_settings_set_entry('-foldernames-', list(
                    set(sg.user_settings_get_entry('-foldernames-', []) + [self.values['-FOLDERNAME-'], ])))
                sg.user_settings_set_entry('-last foldername-', self.values['-FOLDERNAME-'])
                data = datetime.now()
                data = data.strftime("%d-%m-%Y")
                self.pastabkp = self.values['-FOLDERNAME-'].rstrip() + '/'
                self.nomearq = 'database-' + data
                arquivo = self.pastabkp + self.nomearq
                data = datetime.now()
                data = data.strftime("%d/%m/%Y")
                sg.user_settings_set_entry('-lastbackup-', data)
                # print(self.nomearqorig)
                # print(self.nomearqbkp)
                print(self.enderecopai)
                print(self.nomedapasta)
                print(arquivo)
                try:
                    shutil.make_archive(base_name=arquivo, root_dir=os.getcwd(),
                                        base_dir=self.nomedapasta, format='zip')
                    sg.popup('Arquivo compactado gerado com sucesso.')
                except OSError:
                    sg.popup('Erro na criação do arquivo compactado.')
        self.window.close()


# FINAL TELA DE BACKUP

# INICIO BACKUP COMPLETO
class BackupCompleto:
    pastabkp = ''
    endereco = os.getcwd()
    nomearq = ''
    nomedapasta = os.path.basename(endereco)
    enderecopai = os.path.dirname(endereco)

    def __init__(self):
        self.values = None
        self.event = None
        self.layout = [
            [sg.Image(source=icones[1]),
             sg.Text('Cópia de segurança completa', font='_ 25')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.T('Esta função gera um arquivo compactado.')],
            [sg.T('De preferência, use como destino um drive removível (pendrive).')],
            [sg.Text('Selecione a pasta onde deseja guardar uma cópia do sistema:')],
            [sg.Combo(sorted(sg.user_settings_get_entry('-pastasbkpcompleto-', [])),
                      default_value=sg.user_settings_get_entry('-ultimapastabkpcompleto-', ''), size=(50, 1),
                      key='-NOMEDAPASTA-'), sg.FolderBrowse('Abrir pasta...')],
            [sg.Push(), sg.Button('Gerar cópia', k='-BACKUP-'), sg.Button('Sair', k='-SAIR-')]
        ]

        self.window = sg.Window('Cópia de segurança', self.layout, )

    def run(self):
        while True:
            self.event, self.values = self.window.read()
            if self.event in (sg.WIN_CLOSED, '-SAIR-'):
                break
            if self.event == '-BACKUP-':
                sg.user_settings_set_entry('-pastasbkpcompleto-', list(
                    set(sg.user_settings_get_entry('-pastasbkpcompleto-', []) + [self.values['-NOMEDAPASTA-'], ])))
                sg.user_settings_set_entry('-ultimapastabkpcompleto-', self.values['-NOMEDAPASTA-'])
                data = datetime.now()
                data = data.strftime("%d-%m-%Y")
                # self.pastabkp = self.values['-NOMEDAPASTA-'].rstrip() + '/' + 'sistema' + data
                self.pastabkp = self.values['-NOMEDAPASTA-'].rstrip() + '/'
                self.nomearq = 'sistema-' + data
                arquivo = self.pastabkp + self.nomearq
                try:
                    shutil.make_archive(base_name=arquivo, root_dir=self.enderecopai,
                                        base_dir=self.nomedapasta, format='zip')
                    sg.popup('Arquivo compactado gerado com sucesso.')
                except OSError:
                    sg.popup('Erro na criação do arquivo compactado.')
                # print(self.nomearqbkp)
                # try:
                #    shutil.copyfile(self.nomearqorig,self.nomearqbkp)
                #    sg.popup('Arquivo gravado com sucesso.')
                # except:
                #    sg.popup('Erro durante a gravação do arquivo.')
        self.window.close()


# FINAL BACKUP COMPLETO

#######################################
# RELATORIOS
#######################################

# INICIO DE RELATORIO DE PAGAMENTO MENSAL
class RelatorioMensal:
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro',
             'Outubro', 'Novembro', 'Dezembro']
    rot_tabela = ['Data', 'Aluno', 'Atr.', 'Valor']  # Atr. = atraso
    largcol = [10, 25, 5, 10]
    primeiro = True

    def __init__(self):
        self.values = None
        self.event = None
        self.layout = [
            [sg.Image(source=icones[0]),
             sg.Text('Relatório de pagamentos do mês', font='_ 25', key='-TITULO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.Text('Mês desejado:'), sg.Combo(meses, key='-MES-', default_value=mesatual(), enable_events=True),
             sg.T('Ano:'), sg.I(default_text='2022', s=(10, 1), k='-ANO-')],
            [sg.Table(values=[], headings=self.rot_tabela,
                      # max_col_width=15,
                      auto_size_columns=False,
                      col_widths=self.largcol,
                      num_rows=15,
                      def_col_width=10,
                      alternating_row_color='lightblue4',
                      key='-TABLE-',
                      selected_row_colors='black on lightblue1',
                      enable_events=True,
                      expand_x=True,
                      expand_y=True,
                      enable_click_events=True
                      )],
            [sg.Push(), sg.T('Valor total recebido:'), sg.I(k='-TOTAL-', disabled=True, s=(10, 1))],
            [sg.Push(), sg.Button('Gerar relatório', key='-GERA-', bind_return_key=True),
             sg.Button('Imprimir', key='-IMPRIME-', disabled=True), sg.Button('Fechar', key='-FECHAR-')]

        ]

        self.window = sg.Window('Relatório mensal', self.layout, size=(
            700, 500), finalize=True)  # return_keyboard_events=True, enable_close_attempted_event=True modal=True,

    def run(self):
        while True:
            tmptabela = self.window['-TABLE-'].Values
            tabela_final = sort_table(tmptabela, (0,))
            self.window['-TABLE-'].update(tabela_final)

            if self.primeiro:
                mesano = datetime.strftime(datetime.now(), '%m/%Y')
                # self.window['-TABLE-'].update(rel_fin_mensal(mesano))
                self.window['-TABLE-'].update('')
                self.window['-TABLE-'].update(mensalidades_relatorio(mesano))
                calc_val_rec = mensalidades_relatorio(mesano)
                val_rec = 0.00
                i = 0
                while i < len(calc_val_rec):
                    valor = calc_val_rec[i][3]
                    # valor = valor.replace(',', '.')
                    val_rec = val_rec + float(valor)
                    # print(val_rec)
                    i = i + 1
                # valfinal = str(val_rec).replace('.', ',')
                # valfinal = valfinal + '0'
                self.window['-TOTAL-'].update(locale.currency(val_rec))
                tmptabela = self.window['-TABLE-'].Values
                tabela_final = sort_table(tmptabela, (0,))
                self.window['-TABLE-'].update(tabela_final)
                self.primeiro = False

            self.event, self.values = self.window.read()

            if self.event in (sg.WIN_CLOSED, '-FECHAR-'):
                break

            mes = 0
            mesano = ''
            if self.values['-MES-'].rstrip() == 'Janeiro':
                mes = 1
            elif self.values['-MES-'].rstrip() == 'Fevereiro':
                mes = 2
            elif self.values['-MES-'].rstrip() == 'Março':
                mes = 3
            elif self.values['-MES-'].rstrip() == 'Abril':
                mes = 4
            elif self.values['-MES-'].rstrip() == 'Maio':
                mes = 5
            elif self.values['-MES-'].rstrip() == 'Junho':
                mes = 6
            elif self.values['-MES-'].rstrip() == 'Julho':
                mes = 7
            elif self.values['-MES-'].rstrip() == 'Agosto':
                mes = 8
            elif self.values['-MES-'].rstrip() == 'Setembro':
                mes = 9
            elif self.values['-MES-'].rstrip() == 'Outubro':
                mes = 10
            elif self.values['-MES-'].rstrip() == 'Novembro':
                mes = 11
            elif self.values['-MES-'].rstrip() == 'Dezembro':
                mes = 12

            if self.event == '-GERA-' or self.event == '-MES-':
                mesano = str(mes) + '/' + str(self.values['-ANO-'].rstrip())
                # self.window['-TABLE-'].update(rel_fin_mensal(mesano))
                self.window['-TABLE-'].update('')
                self.window['-TABLE-'].update(mensalidades_relatorio(mesano))
                calc_val_rec = mensalidades_relatorio(mesano)
                val_rec = 0.00
                i = 0
                while i < len(calc_val_rec):
                    valor = calc_val_rec[i][3]
                    # valor = valor.replace(',', '.')
                    val_rec = val_rec + float(valor)
                    # print(val_rec)
                    i = i + 1
                # valfinal = str(val_rec).replace('.', ',')
                # valfinal = valfinal + '0'
                self.window['-TOTAL-'].update(locale.currency(val_rec))
                self.window['-IMPRIME-'].update(disabled=False)

            if self.event == '-IMPRIME-':
                pdfgen.gera_relatorio_pdf(
                    str(self.values['-MES-'].rstrip()), self.values['-ANO-'].rstrip(),
                    self.values['-TOTAL-'].rstrip(), mensalidades_relatorio(mesano))

                self.window.perform_long_operation(lambda: os.system('\"' + pdfviewer + '\" ' + pdfgen.arq_relatorio),
                                                   '-FUNCTION COMPLETED-')

        self.window.close()


# FINAL DE RELATORIO DE PAGAMENTO MENSAL

# INICIO DE RELATORIO DE NAO PAGADORES MENSAL # EDITANDO
class RelNaoPago:
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro',
             'Outubro', 'Novembro', 'Dezembro']
    rot_tabela = ['Índice', 'Aluno', 'Mês em haver', 'Valor', 'Atraso']  # atraso é o tempo que está atrasada a mens.
    larg_col = [5, 25, 0, 15, 12]
    tabela_relatorio = None

    def __init__(self):
        self.values = None
        self.event = None
        self.layout = [
            [sg.Text('Relatório de não pagadores', font='_ 25', key='-TITULO-')],
            [sg.HorizontalSeparator(k='-SEP-')],
            [sg.Text('Mês desejado:'), sg.Combo(meses, key='-MES-',
                                                default_value=datetime.now().strftime('%B').capitalize(),
                                                enable_events=True),
             sg.T('Ano:'),
             sg.I(default_text=datetime.now().strftime('%Y'), s=(10, 1), k='-ANO-')],
            [sg.Table(values=[], headings=self.rot_tabela, col_widths=self.larg_col,
                      # max_col_width=15,
                      visible_column_map=[True, True, False, True, True],
                      auto_size_columns=False,
                      num_rows=15,
                      def_col_width=10,
                      # alternating_row_color='lightblue4',
                      key='-TABLE-',
                      # selected_row_colors='black on lightblue1',
                      enable_events=True,
                      expand_x=True,
                      expand_y=True,
                      enable_click_events=True,
                      bind_return_key=True
                      )],
            [sg.T('Clique 2x no aluno para receber mensalidade.'), sg.Push(),
             sg.T('Valor total devido:'), sg.I(k='-TOTAL-', disabled=True, s=(10, 1))],
            [sg.Push(), sg.Button('Gerar relatório', key='-GERA-', bind_return_key=True),
             sg.B('Imprimir relatório', k='-IMPRIME-', disabled=True),
             sg.Button('Fechar', key='-FECHAR-')]

        ]

        self.window = sg.Window('Relatório mensal', self.layout, size=(
            700, 500), finalize=True)  # return_keyboard_events=True, enable_close_attempted_event=True modal=True,

        self.window["-TABLE-"].bind('<Double-Button-1>', "+-double click-")

    def run(self):
        while True:
            self.event, self.values = self.window.read()

            print(self.event, self.values)

            if self.event == '-TABLE-':
                self.row = self.values[self.event]
                self.dados = self.window['-TABLE-'].Values

            if self.event == '-TABLE-+-double click-':
                # sg.popup('Double click on ', self.dados[self.row[0]][0])
                obj_recebe = Pagamentos()
                obj_recebe.indicealuno = self.dados[self.row[0]][0]
                obj_recebe.nomealuno = self.dados[self.row[0]][1]
                obj_recebe.run()

            if self.event == '-GERA-':
                mesano = str(mes_numero(str(self.values['-MES-'].rstrip())) + '/' + str(self.values['-ANO-'].rstrip()))
                mensalidades_devidas = mensalidades_relatorio_devidas(mesano)
                tabela_tmp = []
                self.tabela_relatorio = []
                valortotal = 0.0
                for idx, x in enumerate(mensalidades_devidas):
                    data_vencto = str(x[3]) + '/' + mesano
                    atraso_timedelta = (datetime.now() - datetime.strptime(data_vencto, '%d/%m/%Y'))
                    atraso = str(atraso_timedelta.days)
                    if int(atraso) < 0:
                        atraso = '0'
                    tabela_tmp.append([x[0], x[1], self.values['-MES-'].rstrip(), locale.currency(float(x[2])), atraso])
                    self.tabela_relatorio.append([x[0], x[1], atraso])
                    valortotal += float(x[2])
                self.window['-TABLE-'].Update(values=tabela_tmp)
                self.window['-TOTAL-'].Update(value=locale.currency(valortotal))
                self.window['-IMPRIME-'].update(disabled=False)

            if self.event == '-IMPRIME-':
                if self.tabela_relatorio:
                    mes_ano = self.values['-MES-'].rstrip() + ' de ' + str(self.values['-ANO-'].rstrip())
                    pdfgen.gera_lista_dividas(self.tabela_relatorio, mes_ano)
                    self.window.perform_long_operation(
                        lambda: os.system('\"' + pdfviewer + '\" ' + pdfgen.arq_lista),
                        '-FUNCTION COMPLETED-')

            if self.event == sg.WIN_CLOSED or self.event == '-FECHAR-':
                break

        self.window.close()


# FINAL DE RELATORIO DE NAO PAGADORES MENSAL

############################################
# PRINCIPAL
sg.user_settings_filename(path=ajustes)
# splashscreen()
mensalidades_criar()
ObjPrincipal = Principal()
ObjPrincipal.run()
############################################


# print('DBFILE',dbfile)
# print(os.getcwd())
# ObjRecebe = Recebe()
# ObjRecebe.indicealuno = 2
# ObjRecebe.run()

# ObjCadastro = CadastroAluno()
# ObjCadastro.run()
# geravencto(10)

# ObjRelMen = RelatorioMensal()
# ObjRelMen.run()
# variavel = '06/2022'
# rel_fin_mensal(variavel)
# ObjBackupDB = BackupDB()
# ObjBackupDB.run()
# gera_recibo_pdf('Zé das Couves','100,00','10/10/2010','10/10/2010','0','Andréia')

# ObjMaisInfo = MaisInfo()
# ObjMaisInfo.indice = 1
# ObjMaisInfo.run()

# print(pdfviewer)
# temp = '\"'+pdfviewer + '\" ' + arq_recibo
# print('\"'+pdfviewer + ' ' + arq_recibo+'\"')
# print(temp)
# os.system(temp)


# ObjBackupCompleto = BackupCompleto()
# ObjBackupCompleto.run()
