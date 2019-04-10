import rpyc

conn = rpyc.classic.connect("localhost")

#Faça um programa que leia o nome, o sexo e a idade de uma pessoa e determine se
#a pessoa já atingiu a maioridade sabendo-se que: as pessoas do sexo masculino
#atingem a maioridade aos 18 anos e as pessoas do sexo feminino atingem a
#maioridade aos 21 anos. O programa deve escrever o resultado encontrado

my_code = '''
def maioridade(sexo,idade):
    if idade >=18 and sexo =="masculino": 
       return "de maior"
    elif idade < 18 and sexo =="masculino":
       return "de menor"
    elif idade >=21 and sexo =="feminino":
       return "de maior"
    elif idade < 21 and sexo =="feminino":
       return "de menor"
'''
conn.execute(my_code)

nb = input("Digite o nome da pessoa: ")
nome = str(nb)

nb = input("Digite o sexo da pessoa: ")
sexo = str(nb)

nb = input("Digite a idade da pessoa: ")
idade = int(nb)

rf = conn.namespace['maioridade']

print(nome + " é",rf(sexo, idade))


