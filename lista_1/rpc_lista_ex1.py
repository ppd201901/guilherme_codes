# Iniciar o servidor: ./rpyc_classic.py -m threaded -p 18812
import rpyc

conn = rpyc.classic.connect("localhost")

#Faça um programa que leia o nome, o cargo e o salário de um funcionário e escreva
#seu salário reajustado. Se o cargo do funcionário for operador, ele deverá receber
#um reajuste de 20%, se for programador, ele deverá receber um reajuste de 18%. O
#programa deve escrever o nome do funcionário e seu salário reajustado.

my_code = '''
def reajuste(cargo,sal):
    if cargo == "programador": 
       return (sal+sal*0.18)
    elif cargo == "operador":
        return (sal+sal*0.20)
    else:
        return 0
'''
conn.execute(my_code)

nb = input("Digite o nome do funcionário: ")
nome = str(nb)

nb = input("Digite o cargo do funcionário: ")
cargo = str(nb)

nb = input("Digite o salário do funcionário: ")
sal = float(nb)

rf = conn.namespace['reajuste']

print("O novo salário é", rf(cargo, sal))