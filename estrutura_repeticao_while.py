opcao = int(input("Digite <1>=extrato, <2>=Saldo, <0> para sair: "))

while opcao != 0:
    if opcao == 1:
        print(f"Você escolheu a opção {opcao} de extrato.")
    elif opcao == 2:
        print(f"Você escolheu a opção {opcao} de saldo.")
    else:
        print("Opção inválida. Tente novamente.")

    # O input precisa estar aqui dentro, para atualizar a variável 'opcao'
    opcao = int(input("Digite <1>=extrato, <2>=Saldo, <0> para sair: "))

print("finalizando o programa.")    
  