f = open("1.txt", "r")
lista = f.readlines()

print(lista)

salida = []
for elemento in lista:
    if '\n' in elemento:
        aux = elemento.replace('\n','')
        salida.append(float(aux))

print(salida)
f.close()