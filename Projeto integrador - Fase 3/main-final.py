# Projeto Integrador │ Fase 2

# Requisitos para o funcionamento do sistema: Abra o terminal e digite os seguintes comandos: "pip install pandas", "pip install oracledb" e "pip install unidecode" (Instalação da biblioteca referente a tabela e banco de dados) 

import sys
import time
import pandas as pd
from unidecode import unidecode

# Cripto
import numpy as np
import os

# Banco de dados
import getpass
import oracledb


# Cleaner Prompt
def clear_screen():
    os.system('cls')
clear_screen()
# Cleaner Prompt end

alfabeto = {' ': 0,'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26}

def criptografar(descricao):
    palavra = f'{unidecode(descricao)}'.upper()
    palavra_impar = False
    if len(palavra) % 2 != 0:
        palavra += "A"
        palavra_impar = True

    matriz_palavra_em_num = palavra_em_matriz(palavra)

    palavra_original = palavra[:-1] if palavra_impar else palavra
    # print("-" * 50)
    # print(f"Matriz da palavra {palavra_original} em números:")
    # print(matriz_palavra_em_num)
    # # print("-" * 50)

    chaveMatriz = np.array([[4, 3], [1, 2]])
    criptografada = np.dot(chaveMatriz, matriz_palavra_em_num) % 26
    # print(f"Matriz da palavra {palavra_original} criptografada:")
    # print(criptografada)
    # print("-" * 50)
    palavra_criptografada = monta_palavra(criptografada, palavra_impar)
    print(f"{palavra_original} = {palavra_criptografada}")

    return palavra_criptografada
def palavra_em_matriz(palavra):
    letras = []
    for letra in palavra:
        letras.append(alfabeto[letra])
    matriz_palavra_em_num = np.array(letras)
    if len(matriz_palavra_em_num) % 2 != 0:
        matriz_palavra_em_num = np.append(matriz_palavra_em_num, [0]) 
    matriz_palavra_em_num = matriz_palavra_em_num.reshape(2, -1, order='F')
    return matriz_palavra_em_num

def monta_palavra(matriz, palavra_impar):
    palavra_formada = ''
    for coluna in matriz.T:
        for num in coluna:
            if num == 0:
                palavra_formada += ' '
            else:
                palavra_formada += list(alfabeto.keys())[list(alfabeto.values()).index(num)]
    if palavra_impar:
        palavra_formada = palavra_formada[:-1]
    return palavra_formada

def decifrar():
    palavra_criptografada = input("Digite a palavra criptografada: ").upper()

    matriz_palavra_em_num = palavra_em_matriz(palavra_criptografada)
    a, b, c, d = 4, 3, 1, 2
    chaveMatrizInversa = np.array([[d, -b], [-c, a]])
    det = (a * d) - (b * c)
    det_inversas = {1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25}
    det_inv = det_inversas[det % 26]
    chaveMatrizInversa = (chaveMatrizInversa * det_inv) % 26

    matriz_palavra_em_num = np.dot(chaveMatrizInversa, matriz_palavra_em_num) % 26

    palavra_original = monta_palavra(matriz_palavra_em_num, len(palavra_criptografada) % 2 != 0)  # Corrigindo a lógica de remoção do último caractere

    print("Mensagem descriptografada:")
    print(palavra_original)

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

def menu() :
    # Menu de navegação
    loading_bar()
    menu = ["1. Cadastrar produto","2. Alterar produtos", "3. Excluir produto", "4. Classificar produtos", "5. Sair"]
    # Mostrar o menu e input para selecionar a opção
    print (menu)

# 1
def adicionar_produto () :
    # Criar cursor e commitar alterações (Nenhuma alteração no caso)
    cursor = conexao.cursor()
    loading_bar()
    
    print (f"Vamos ao cadastro do seu produto, preencha as informações abaixo: ")
    id_produto = str (input("Digite o código do produto: "))
    nome = str (input("Digite o nome do produto: "))
    descricao = str (input("Digite a descrição do produto: ")) # Colocar a func codificadora aqui

    palavra_criptografada = criptografar(descricao)
    
    decifrar()
    # Perguntas para montar a fórmula de cálculo do preço de venda
    loading_bar()
    print (f"Agora, precisamos de algumas informações para o levantamento de dados:")
    
    CP = int (input("Qual custo de aquisição do produto?: "))
    CF = int (input("Qual o custo fixo/administrativo? (em porcentagem):  "))
    CV = int(input("Qual a comissão de venda do produto? (em porcentagem):  "))
    IV = int(input("Qual o imposto cobrado sobre a venda do produto? (em porcentagem): "))
    ML = int(input("Qual a margem do lucro do produto? (em porcentagem):  "))

    #Executar comando no banco de dados
    cursor.execute(f"INSERT INTO Produtos (ID, NOME, DESCRICAO, CP, CF, CV, IV, ML) VALUES ({id_produto}, '{nome}', '{palavra_criptografada}', {CP}, {CF}, {CV}, {IV}, {ML})")
    conexao.commit()
    # Fechar cursos
    cursor.close()
    
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
    loading_bar()

    
    tabela = pd.DataFrame({"Descrição": ["Preço de venda","Custo de aquisição(Fornecedor)","Receita bruta(A-B)","Custo Fixo/Administrativo","Comissão de vendas","Impostos", "Outros custos(D + E + F)", "Rentabilidade"],
                   "Valor": [PV, CP, RB, PCF, PCV, PIV, POC, PML],
                   "%": [PPV, PCP, PRB, CF, CV, IV, OC, ML]})
    
    print(f"\nID do Produto: {id_produto}\nProduto: {nome}\nDescrição: {palavra_criptografada}\n{tabela} \n")
    print ("-" * 55)

    # Passando a margem de lucro (ML) para porcentagem
    lucro = ML/100

    if lucro > (0.2):
        print("Lucro alto!")
    elif (0.1) < lucro <= (0.2):
        print("Lucro médio!")
    elif (0) < lucro <= (0.1):
        print("Lucro baixo!")
    elif lucro == 0:
        print("Equilíbrio!")
    else:
        print("Prejuízo!")

# 2
def alterar_produto () :
    # Criar cursor e commitar alterações (Nenhuma alteração no caso)
    cursor = conexao.cursor()
    #Executar comando no banco de dados 
    cursor.execute("SELECT * FROM Produtos")
    # Salvar o que o comando "cursor.excute" fez. Todos as informações de "Produtos" foram salva na variável "lista_produtos"
    dict_classificar_produtos = cursor.fetchall() 
    # Fechar cursos
    cursor.close()
    ids = []
    loading_bar()
    # Loop para pegar os dados da tabela "Produtos" no DB.
    for i in dict_classificar_produtos:
        
        # Atribuir das tuplas a variável "i" -- Será atribuido a cada uma das variaveis as tuplas correspondentes a lista "lista_produtos".
        id_produto, nome, descricao, CP, CF, CV, IV, ML = i
        ids.append(id_produto)
        print (f"ID: {id_produto} │ Nome: {nome} │ Descrição: {descricao} │ CP: R${CP} │ CF: {CF}% │ CV: {CV}% │ IV: {IV}% │ ML: {ML}%")
    while True:
        try:
            alterar = str (input("\nQual o ID do produto que deseja alterar? "))
            loading_bar()
            if alterar not in ids:
                raise ValueError("Esse ID não existe na tabela. Digite um ID válido.")
            else :
                # Criar cursor e commitar alterações (Nenhuma alteração no caso)
                cursor = conexao.cursor()
                #Executar comando no banco de dados 
                cursor.execute(f"SELECT * FROM Produtos WHERE ID = {alterar}")
                # Salvar o que o comando "cursor.excute" fez. Todos as informações de "Produtos" foram salva na variável "lista_produtos"
                dict_produto_selecionado = cursor.fetchall() 
                # Loop para pegar os dados da tabela "Produtos" no DB.
                for i in dict_produto_selecionado:
                    # Atribuir das tuplas a variável "i" -- Será atribuido a cada uma das variaveis as tuplas correspondentes a lista "lista_produtos".
                    id_produto, nome, descricao, CP, CF, CV, IV, ML = i

                print (f"\nID: {id_produto} │ Nome: {nome} │ Descrição: {descricao} │ CP: R${CP} │ CF: {CF}% │ CV: {CV}% │ IV: {IV}% │ ML: {ML}% \n")

                oque_alterar = input ("O que deseja alterar? ")
                set_alterar = input(f"Qual o novo valor para {oque_alterar.upper()}?")

                cursor.execute(f"UPDATE Produtos SET {unidecode(oque_alterar.upper())} = '{set_alterar}' WHERE ID = '{id_produto}'")
                conexao.commit()

                cursor.execute(f"SELECT * FROM Produtos WHERE ID = {id_produto}")

                # Salvar o que o comando "cursor.excute" fez. Todos as informações de "Produtos" foram salva na variável "lista_produtos"
                produto_alterado = cursor.fetchall()

                for i in produto_alterado:
                    # Atribuir das tuplas a variável "i" -- Será atribuido a cada uma das variaveis as tuplas correspondentes a lista "lista_produtos".
                    id_produto, nome, descricao, CP, CF, CV, IV, ML = i
                loading_bar()
                print (f"\nConfira seu produto com as alterações realizadas:")
                print (f"\nID: {id_produto} │ Nome: {nome} │ Descrição: {descricao} │ CP: R${CP} │ CF: {CF}% │ CV: {CV}% │ IV: {IV}% │ ML: {ML}%\n")

                # Fechar cursor
                cursor.close()
                
                break
                
        except ValueError as erro:
            print(erro)

def excluir_produto ():
    # Criar cursor e commitar alterações (Nenhuma alteração no caso)
    cursor = conexao.cursor()
    #Executar comando no banco de dados 
    cursor.execute("SELECT * FROM Produtos")
    # Salvar o que o comando "cursor.excute" fez. Todos as informações de "Produtos" foram salva na variável "lista_produtos"
    dict_classificar_produtos = cursor.fetchall() 
    # Fechar cursos
    cursor.close()
    ids = []
    loading_bar()
    # Loop para pegar os dados da tabela "Produtos" no DB.
    for i in dict_classificar_produtos:
        
        # Atribuir das tuplas a variável "i" -- Será atribuido a cada uma das variaveis as tuplas correspondentes a lista "lista_produtos".
        id_produto, nome, descricao, CP, CF, CV, IV, ML = i

        ids.append(id_produto)
        print (f"ID: {id_produto} │ Nome: {nome} │ Descrição: {descricao} │ CP: R${CP} │ CF: {CF}% │ CV: {CV}% │ IV: {IV}% │ ML: {ML}%")
    while True:
        try:
            alterar = str (input("\nQual o ID do produto que deseja excluir? "))
            loading_bar()
            if alterar not in ids:
                raise ValueError("Esse ID não existe na tabela. Digite um ID válido.")
            else :
                # Criar cursor e commitar alterações (Nenhuma alteração no caso)
                cursor = conexao.cursor()
                #Executar comando no banco de dados 
                cursor.execute(f"SELECT * FROM Produtos WHERE ID = {alterar}")
                # Salvar o que o comando "cursor.excute" fez. Todos as informações de "Produtos" foram salva na variável "lista_produtos"
                dict_produto_selecionado = cursor.fetchall() 
                # Loop para pegar os dados da tabela "Produtos" no DB.
                for i in dict_produto_selecionado:
                    # Atribuir das tuplas a variável "i" -- Será atribuido a cada uma das variaveis as tuplas correspondentes a lista "lista_produtos".
                    id_produto, nome, descricao, CP, CF, CV, IV, ML = i

                print (f"\nID: {id_produto} │ Nome: {nome} │ Descrição: {descricao} │ CP: R${CP} │ CF: {CF}% │ CV: {CV}% │ IV: {IV}% │ ML: {ML}% \n")
                
                ctz = (input("Tem certeza que deseja excluir esse produto?S/N "))
                if ctz == 's' or 'S' or 'sim' or 'Sim':
                    cursor.execute(f"DELETE FROM Produtos Where ID = {id_produto}")
                    print (f"\nExcluindo:", end=" ")
                    loading_bar()
                    print (f"\n{nome.capitalize()} foi excluído!")
                    conexao.commit()
                    cursor.execute(f"SELECT * FROM Produtos")
                    # Salvar o que o comando "cursor.excute" fez. Todos as informações de "Produtos" foram salva na variável "lista_produtos"
                    pos_excluir = cursor.fetchall() 
                    # Loop para pegar os dados da tabela "Produtos" no DB.
                    print (f"\nConfira sua lista de produtos atualizada: \n")
                    for i in pos_excluir:
                        # Atribuir das tuplas a variável "i" -- Será atribuido a cada uma das variaveis as tuplas correspondentes a lista "lista_produtos".
                        id_produto, nome, descricao, CP, CF, CV, IV, ML = i
                        print (f"ID: {id_produto} │ Nome: {nome} │ Descrição: {descricao} │ CP: R${CP} │ CF: {CF}% │ CV: {CV}% │ IV: {IV}% │ ML: {ML}%")
                    print ("\n")
                else :
                    loading_bar()
                break
                
        except ValueError as erro:
            print(erro)

def classificar_produtos():
    # Criar cursor e commitar alterações (Nenhuma alteração no caso)
    cursor = conexao.cursor()
    #Executar comando no banco de dados 
    cursor.execute("SELECT * FROM Produtos")
    # Salvar o que o comando "cursor.excute" fez. Todos as informações de "Produtos" foram salva na variável "lista_produtos"
    lista_produtos = cursor.fetchall() 
    # Fechar cursos
    cursor.close()

    # Loop para pegar os dados da tabela "Produtos" no DB.
    for i in lista_produtos:
        # Atribuir das tuplas a variável "i" -- Será atribuido a cada uma das variaveis as tuplas correspondentes a lista "lista_produtos".
        id_produto, nome, descricao, CP, CF, CV, IV, ML = i

        if (ML >= 100) :
            #Fórmula para calcular o preço de venda se ML for maior ou igual a 100
            PV = CP * ( 1 + ( ( CF + CV + IV + ML ) / 100 ) )
    
        elif (ML < 100) :
            #Fórmula para calcular o preço de venda se ML for menor que 100
            PV = CP / ( 1 - ( ( CF + CV + IV + ML ) / 100 ) )

        # Receita Bruta é = Preço de Venda - Custo do produto
        RB = (PV - CP)

        # Outros custos = Custo fixo + Comissão de vendas + Imposto sobre venda
        OC = (CF + CV + IV)

        # Lógica 1
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

        tabela = pd.DataFrame({"Descrição": ["A. Preço de venda","B. Custo de aquisição(Fornecedor)","C. Receita bruta(A-B)","D. Custo Fixo/Administrativo","E. Comissão de vendas","F. Impostos", "G. Outros custos(D + E + F)", "H. Rentabilidade"],
                               "Valor": [PV, CP, RB, PCF, PCV, PIV, POC, PML],
                               "%": [PPV, PCP, PRB, CF, CV, IV, OC, ML]})
        
        print(f"\nID do Produto: {id_produto}\nProduto: {nome}\nDescrição: {descricao}\n{tabela} \n", "-" * 45 )

        #Função Lucro
        lucro(ML)

def lucro(ML):
    # Passando a margem de lucro (ML) para porcentagem
        lucro = ML/100

        if lucro > (0.2):
            print("Lucro alto!")
        elif (0.1) < lucro <= (0.2):
            print("Lucro médio!")
        elif (0) < lucro <= (0.1):
            print("Lucro baixo!")
        elif lucro == 0:
            print("Equilíbrio!")
        else:
            print("Prejuízo!")

def sair():
    print ("Saindo...")
    sys.exit()


# Banco de dados Oracle

while True :
    try:
        pw = getpass.getpass("Digite a senha: ")
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

    menu()
    opcao = int (input("Escolha uma opção: "))

    if opcao == 1 :
         adicionar_produto()

    elif opcao == 2 :
        alterar_produto()

    elif opcao == 3 :
        excluir_produto()

    elif opcao == 4 :
        classificar_produtos()
        
    else :
        sair()
         