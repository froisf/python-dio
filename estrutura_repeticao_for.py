texto = input("Digite um texto: ")
VOGAIS = "AEIOU"

for letras in texto:
     if letras.upper() not in VOGAIS:
        print(letras, sep="", end="-")
else:

  print("\nFim do processamento.")        

  for numero in range(0, 51, 5):
      print(numero, sep="", end="-")
  else:
      print("\nFim do processamento.")
