# Projeto Integrador │ Fase 3


import os
import sys
import time

import pandas as pd
from tabulate import tabulate

from unidecode import unidecode

import numpy as np

import getpass
import oracledb

# Cleaner Prompt
def clear_screen():
    os.system('cls')
clear_screen()
# Cleaner Prompt end

ids = []

alfabeto = {' ': 0,'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26}

def menu() :
    # Menu de navegação
    loading_bar()
    print ("\nBem vindo ao sistema de Controle de Estoque, Cálculo de preço de venda, Percentuais e Classificação de lucro. \n")
    print ("1. Cadastrar produto \n2. Alterar produtos \n3. Excluir produto \n4. Classificar produtos \n0. Sair")

def criptografar(descricao):
    palavra = f'{unidecode(descricao)}'.upper()
    
    palavra_impar = False

    # Se a palavra for impar, adicionar um 'A' para ficar par.
    if len(palavra) % 2 != 0:
        palavra += "A"
        palavra_impar = True

    # Converte a palavra, descrição no caso, em uma matriz de números.
    matriz_palavra_em_num = palavra_em_matriz(palavra)

    # Definindo a matriz chave
    chaveMatriz = np.array([[4, 3], [1, 2]])

    # Multiplicando a matriz chave pela matriz da descrição e aplicando o módulo de 26.
    criptografada = np.dot(chaveMatriz, matriz_palavra_em_num) % 26
    
    # Montando a palavra a partir da matriz resultante
    palavra_criptografada = monta_palavra(criptografada, palavra_impar)

    return palavra_criptografada

def palavra_em_matriz(palavra):
    letras = []

    # Lendo a descrição, verificando o valor correspondente e adicionar em 'letras' o valor correspondente as letras de descrição. 
    for letra in palavra:
        letras.append(alfabeto[letra])

    # Convertendo em um array para realizar os calculos.
    matriz_palavra_em_num = np.array(letras)

    # Impar ou não (Se for impar, adiciona o valor 0 ao final do array.)
    if len(matriz_palavra_em_num) % 2 != 0:
        matriz_palavra_em_num = np.append(matriz_palavra_em_num, [0]) 

    # Pega o array e transforma em uma matriz c/ 2 linhas, -1 para determinar o número de colunas automaticamente e 'F' para ordernar os números coluna por coluna.
    matriz_palavra_em_num = matriz_palavra_em_num.reshape(2, -1, order='F')

    return matriz_palavra_em_num

def monta_palavra(matriz, palavra_impar):
    # Defininindo a variável da palavra que será formada a partir da matriz.
    palavra_formada = ''
    
    # Loop da transposta da Matriz
    for coluna in matriz.T:
        # Verificando na matriz o número (Através das colunas)
        for num in coluna:
            if num == 0:
                palavra_formada += ' '
            else:
                palavra_formada += list(alfabeto.keys())[list(alfabeto.values()).index(num)] # Encontrando a letra correspondente ao número 'Num'
    # Se a palavra for impar, elimina o ultimo caracter.            
    if palavra_impar:
        palavra_formada = palavra_formada[:-1]

    return palavra_formada

def decifrar(descricao):
    # Descrição maiuscula
    palavra_criptografada = descricao.upper()

    # Montando a matriz da descrição
    matriz_palavra_em_num = palavra_em_matriz(palavra_criptografada)

    # Matriz inversa da chave original
    a, b, c, d = 4, 3, 1, 2
    chaveMatrizInversa = np.array([[d, -b], [-c, a]])

    # determinante da matriz chave original
    det = (a * d) - (b * c)

    # Mapeia os determinantes possíveis para seus inversos
    det_inversas = {1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25}

    # Inverso
    det_inv = det_inversas[det % 26]

    # Multiplicação da Matriz inversa da chave pelo det inv e aplica %26 para garantir que esteja dentro do alfab.
    chaveMatrizInversa = (chaveMatrizInversa * det_inv) % 26

    # Multiplicação da inversa da Matriz Chave pela matriz da descrição e aplica %26 para garantir que esteja dentro do alfab.
    matriz_palavra_em_num = np.dot(chaveMatrizInversa, matriz_palavra_em_num) % 26

    # Monta a palavra decifrada através da matriz
    palavra_decifrada = monta_palavra(matriz_palavra_em_num, len(palavra_criptografada) % 2 != 0)

    return palavra_decifrada

# Começo da função da barra de carregamento
def loading_bar():
    toolbar_width = 15 #Tamanho da barra
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1))

    for i in range(toolbar_width):
        time.sleep(0.05)
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("\n")
# Fim da função da barra de carregamento

def calculos (CP, CF, CV, IV, ML) :
    if (ML >= 100) or (ML < 100) and (CF + CV + IV + ML >= 100) :
        #Fórmula para calcular o preço de venda se ML for maior ou igual a 100
        PV = CP * ( 1 + ( ( CF + CV + IV + ML ) / 100 ) )

    elif (ML < 100) :
        #Fórmula para calcular o preço de venda se ML for menor que 100
        PV = CP / ( 1 - ( ( CF + CV + IV + ML ) / 100 ) )

    # Receita Bruta é = Preço de Venda - Custo do produto
    RB = (PV - CP)

    # Outros custos = Custo fixo + Comissão de vendas + Imposto sobre venda
    OC = (CF + CV + IV)

    #Lógica 1
    # Cáculo da PORCENTAGEM do preço de venda (Regra de 3)
    PPV = (PV*100) / PV

    # Cáculo da PORCENTAGEM do custo do produto (Regra de 3)
    PCP = (CP*100) / PV

    # Cáculo da PORCENTAGEM da Receita Bruta (Regra de 3)
    PRB = (RB*100) / PV
    # Fim Lógica 1

    # Logica 2 -->
    # Cáculo do VALOR do Imposto sobre Venda (Regra de 3)
    PCF = (CF*PV) / 100

    # Cáculo do VALOR da comissão sobre Venda (Regra de 3)
    PCV = (CV*PV) / 100

    # Cáculo do VALOR do Imposto sobre Venda (Regra de 3)
    PIV = (IV*PV) / 100 
    
    # Cáculo do VALOR de Outros custos (Regra de 3)
    POC = (OC*PV) / 100

    # Cáculo do VALOR da rentabilidade (Regra de 3)
    PML = (ML*PV) / 100
    # Fim Lógica 2

    return PV, RB, OC, PPV, PCP, PRB, PCF, PCV, PIV, POC, PML

def mostrar_produtos(produtos):
    produtos_dicionario = {}
    produtos_lista = []

    for i in produtos :
        id, nome, descricao, CP, CF, CV, IV, ML = i

        # Decifrando a descrição
        descricao_decifrada = decifrar(descricao)

        # Armazenando Id's
        ids.append(id)

        produtos_dicionario[id] = [nome, descricao_decifrada.capitalize(), CP, CF, CV, IV, ML]

    for id, values in produtos_dicionario.items():
        produtos_lista.append({"ID": id, "Nome": values[0], "Descrição": values[1], "Custo de aquisição(Fornecedor)": f"R${values[2]}", "Custo Fixo/Administrativo": f"R${values[3]}", "Comissão de vendas": f"{values[4]}%", "Impostos": f"{values[5]}%", "Rentabilidade": f"{values[6]}%"})

    tabela = pd.DataFrame(produtos_lista)
    print(tabulate(tabela, headers='keys', tablefmt='fancy_grid', showindex=False))    

def mostrar_tabela(id_produto, nome, descricao, CP, CF, CV, IV, ML):

    PV, RB, OC, PPV, PCP, PRB, PCF, PCV, PIV, POC, PML = calculos(CP, CF, CV, IV, ML)

    tabela = pd.DataFrame({
    "": ["Preço de venda", "Custo de aquisição(Fornecedor)", "Receita bruta(A-B)", "Custo Fixo/Administrativo", "Comissão de vendas", "Impostos", "Outros custos(D + E + F)", "Rentabilidade"],

    "Valores": [f"R${PV:.2f}", f"R${CP:.2f}", f"R${RB:.2f}", f"R${PCF:.2f}", f"R${PCV:.2f}", f"R${PIV:.2f}", f"R${POC:.2f}", f"R${PML:.2f}"], 
    
    "%": [f"{PPV:.2f}%", f"{PCP:.2f}%", f"{PRB:.2f}%", f"{CF:.2f}%", f"{CV:.2f}%", f"{IV:.2f}%", f"{OC:.2f}%", f"{ML:.2f}%"]})
    
    print(f"\nID do Produto: {id_produto}\nProduto: {nome}\nDescrição: {descricao.capitalize()}")
    alinhamento = ("left", "left", "left")
    print(tabulate(tabela, headers='keys', tablefmt='fancy_grid', showindex=False, colalign=alinhamento))

def lucro(ML):
    # Passando a margem de lucro (ML) para porcentagem
    lucro = ML/100

    if lucro > (0.2):
        print("Lucro alto!\n")
    elif (0.1) < lucro <= (0.2):
        print("Lucro médio!\n")
    elif (0) < lucro <= (0.1):
        print("Lucro baixo!\n")
    elif lucro == 0:
        print("Equilíbrio!\n")
    else:
        print("Prejuízo!\n")

# 1 
def adicionar_produto () :
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Produtos")
    produtos = cursor.fetchall()
    ids = []
    for i in produtos :
        id, nome, descricao, CP, CF, CV, IV, ML = i
        # Armazenando Id's
        ids.append(id)

    loading_bar()
    print (f"Vamos ao cadastro do seu produto, preencha as informações abaixo: ")
    while True:
        id_produto = input("Digite o código do produto: ")
        if id_produto in ids:
            print("Esse ID já existe no banco de dados, tente novamente!")
        else:
            break
    
    nome = str (input("Digite o nome do produto: "))
    descricao = str (input("Digite a descrição do produto: "))

    loading_bar()
    print (f"Agora, precisamos de algumas informações para o levantamento de dados:")
    CP = int (input("Qual custo de aquisição do produto?: "))
    CF = int (input("Qual o custo fixo/administrativo? (em porcentagem):  "))
    CV = int (input("Qual a comissão de venda do produto? (em porcentagem):  "))
    IV = int (input("Qual o imposto cobrado sobre a venda do produto? (em porcentagem): "))
    ML = int (input("Qual a margem do lucro do produto? (em porcentagem):  "))

    descricao_criptografada = criptografar(descricao)
    
    cursor.execute(f"INSERT INTO Produtos (ID, NOME, DESCRICAO, CP, CF, CV, IV, ML) VALUES ({id_produto}, '{nome}', '{descricao_criptografada}', {CP}, {CF}, {CV}, {IV}, {ML})")
    conexao.commit()

    loading_bar()

    # Tabela
    mostrar_tabela(id_produto, nome, descricao, CP, CF, CV, IV, ML)

    # Lucro
    lucro(ML)
    
    cursor.close()

# 2 
def alterar_produto () :
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Produtos")
    produtos = cursor.fetchall()
    
    mostrar_produtos(produtos)

    while True:
        try:
            id_alterar = input ("\nQual o ID do produto que deseja alterar? ")
            loading_bar()

            if id_alterar not in ids:
                print("Esse ID não existe na tabela. Digite um ID válido.")
            
            else :
                cursor.execute(f"SELECT * FROM Produtos WHERE ID = {id_alterar}")
                produtos = cursor.fetchall()
                mostrar_produtos(produtos)
                
                print ("O que deseja alterar? \n1. ID \n2. Nome \n3. Descrição \n4. Custo de aquisição(Fornecedor) \n5. Custo Fixo/Administrativo \n6. Comissão de vendas \n7. Impostos \n8. Rentabilidade")
                alterar = int (input ("\nDigite aqui: "))

                if alterar == 1 :
                    alterar = 'ID'
                elif alterar == 2 :
                    alterar = 'NOME'
                elif alterar == 3 :
                    alterar = 'DESCRICAO'
                elif alterar == 4 :
                    alterar = 'CP'
                elif alterar == 5 :
                    alterar = 'CF'
                elif alterar == 6 :
                    alterar = 'CV'
                elif alterar == 7 :
                    alterar = 'IV'
                else :
                    alterar = 'ML'

                set_alterar = input (f"Qual o novo valor para {alterar}? ")

                if alterar == 'DESCRICAO' :
                    set_alterar = criptografar(set_alterar)

                cursor.execute(f"UPDATE Produtos SET {alterar} = '{set_alterar}' WHERE ID = '{id_alterar}'")
                conexao.commit()

                print (f"\nAlterando: ", end=" ")
                loading_bar()

                print (f"\n{alterar} atualizado!")

                cursor.execute(f"SELECT * FROM Produtos WHERE ID = {id_alterar}")
                produtos = cursor.fetchall()

                print (f"\nConfira seu produto com a alteração realizada:")
                mostrar_produtos(produtos)                
                break
                
        except ValueError:
            print("Digite somente um número ID válido.")

    # Fechando conexão com o banco de dados
    cursor.close()

# 3
def excluir_produto ():
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Produtos")
    produtos = cursor.fetchall()
    
    mostrar_produtos(produtos)
    
    while True:
        try:
            id_excluir = input ("\nQual o ID do produto que deseja excluir? ")
            loading_bar()

            if id_excluir not in ids:
                print("Esse ID não existe na tabela. Digite um ID válido.")

            else :
                cursor.execute(f"SELECT * FROM Produtos WHERE ID = {id_excluir}")
                produtos = cursor.fetchall() 
                
                mostrar_produtos (produtos)
                
                certeza = input("Tem certeza que deseja excluir esse produto? S/N ")

                if certeza in ['s', 'S', 'sim', 'Sim']:
                    cursor.execute(f"DELETE FROM Produtos Where ID = {id_excluir}")
                    conexao.commit()

                    print (f"\nExcluindo: ", end=" ")
                    loading_bar()

                    print (f"\nProduto excluído!")

                    cursor.execute(f"SELECT * FROM Produtos")
                    produtos = cursor.fetchall()
                    print (f"\nConfira sua lista de produtos atualizada: \n")
                    mostrar_produtos (produtos)
                    break

                else :
                    loading_bar()
                    continue
                
        except ValueError as erro:
            print(erro)

    cursor.close()

# 4
def classificar_produtos():
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Produtos")
    lista_produtos = cursor.fetchall()
    
    for i in lista_produtos:
        id_produto, nome, descricao, CP, CF, CV, IV, ML = i

        descricao = decifrar(descricao)

        mostrar_tabela(id_produto, nome, descricao, CP, CF, CV, IV, ML)

        #Função Lucro
        lucro(ML)

    cursor.close()

# Banco de dados Oracle
while True :
    try:
        pw = getpass.getpass("Digite a senha para entrar no programa: ")
        conexao = oracledb.connect(
        user="sys",
        password=pw,
        dsn="localhost/XEPDB1",
        mode=oracledb.SYSDBA)
    except Exception as erro:
        print('Erro de conexão:', erro)
    else:
        print("Conexão bem sucedida:", conexao.version)
        break


while True:
    try:
        menu()
        opcao = int (input("\nEscolha uma opção: "))

        if opcao == 1 :
            adicionar_produto()

        elif opcao == 2 :
            alterar_produto()

        elif opcao == 3 :
            excluir_produto()

        elif opcao == 4 :
            classificar_produtos()

        elif opcao == 0 :
            print ("Saindo...")
            sys.exit()
            
    except ValueError:
        print("Tente novamente...")