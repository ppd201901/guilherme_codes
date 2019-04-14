import rpyc

#Escreva um programa que leia as três notas (N1, N2 e N3) de um aluno de
#Faculdade e escreva se o mesmo foi aprovado ou reprovado. Considere as regras: se
#a média aritmética M, entre N1 e N2, for maior ou igual a 7,0, o aluno está
#aprovado; se a média aritmética M entre N1 e N2 for maior que 3,0 e menor que
#7,0, o aluno deve fazer a N3. O aluno é aprovado se a média aritmética entre M e
#N3 for maior ou igual a 5,0.

conn = rpyc.classic.connect("localhost")

my_code = '''
def media(N1,N2,N3):
    M = 0
    if (N1+N2)/2 >= 7.0:
       M = 1
    elif (N1+N2)/2 > 3.0 and (N1+N2)/2 < 7.0:
        if ((N1+N2)/2 + N3)/2 >= 5.0:
            M  = 2
    return M
'''
conn.execute(my_code)

rf = conn.namespace['media']

nb = input("Digite a nota 1: ")
nota1 = float(nb)

nb = input("Digite a nota 2: ")
nota2 = float(nb)

nb = input("Digite a nota 3: ")
nota3 = float(nb)


if rf(nota1,nota2,nota3) == 0:
    print("Reprovado")
elif rf(nota1,nota2,nota3) == 2:
    print("Aprovado com N3")
else:
    print("Aprovado")