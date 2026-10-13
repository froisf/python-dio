def sacar(valor):
    saldo = 500
    if valor > saldo:
        print("Saldo insuficiente")
        return
    print("Transação aprovada")

sacar(600)

def depositar(valor):
    saldo = 500
    saldo += valor
 
depositar(500)

