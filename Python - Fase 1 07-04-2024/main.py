# Projeto Integrador │ Fase 1

# Requisitos para funcionamento: Abrir o terminal e digitar o sguinte comando: "pip install pandas" (Instalação da biblioteca referente a tabela) 

import sys
import time
import pandas as pd

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
    
# Menu de navegação
loading_bar()
menu = ["1. Cadastrar produtos","2. Classificar produtos","3. Excluir produto","4. Sair"]

# Mostrar o menu e input para selecionar a opção
print (menu)
opcao = int (input("\n Selecione uma opção: "))

# SE o usuário digitar 1, para cadastrar os produtos, irá mostrar na tela os seguintes inputs.
if opcao == 1 : 
    loading_bar()
    print (f"Vamos ao cadastro do seu produto, preencha as informações abaixo: ")
    codigo = int (input("Digite o código do produto: "))
    nome = str (input("Digite o nome do produto: "))
    descricao = str (input("Digite a descrição do produto: "))

    # Perguntas para montar a fórmula de cálculo do preço de venda
    loading_bar()
    print (f"Agora, precisamos algumas informações para calcular o preço do produto:  ")
    
    CP = int (input("Qual custo de aquisição do produto?: "))
    CF = int (input("Qual o custo fixo/administrativo? (em porcentagem):  "))
    CV = int(input("Qual a comissão de venda do produto? (em porcentagem):  "))
    IV = int(input("Qual o imposto cobrado sobre a venda do produto? (em porcetagem): "))
    ML = int(input("Qual a margem do lucro do produto? (em porcentagem):  "))
    
    #Fórmula para calcular o preço de venda
    PV = CP / ( 1 - ( ( CF + CV + IV + ML) / 100 ) )

    
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
    
    print(tabela)

    # 20/100 = 0,2
    lucro = ML/100

    if lucro > (0.2):
        print("Lucro alto!")
    elif (0.1) < lucro <= (0.2):
        print("Lucro médio!")
    elif (0) > lucro <= (0.1):
        print("Lucro baixo!")
    elif lucro == 0:
        print("Equilíbrio!")
    else:
        print("Prejuízo!")
    

# Função 2 (Ainda não funcional).
if opcao == 2 :
    sys.exit()

# Função 3 (Ainda não funcional).
elif opcao == 3 :
    sys.exit()
    
# Função sair, importado da biblioteca sys.
else :
    sys.exit ()