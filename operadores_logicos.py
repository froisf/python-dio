valor = 200
saldo = 500
limite = 100

if valor > saldo:
    print("Saldo insuficiente")
else:
    if valor > limite:
        print("Valor acima do limite")
    else:
        print("Transação aprovada")

if (valor < saldo  and valor > limite):
    print("Valor informado é maior que limete de saldo")


if (valor > saldo or valor > limite):
    print("Valor informado é maior que limete  e saldo")


if (valor < saldo or valor < limite):
    print("Valor informado é menor que limete e saldo")

