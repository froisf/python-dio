IDADE_MINIMA = 18

idade = int(input("Digite sua idade: "))

if idade < IDADE_MINIMA:
    print("Você não tem a idade mínima para tirar sua carteira de habilitação.")
else:
    print("Você já pode tirar sua carteira de habilitação.")