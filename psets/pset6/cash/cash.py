from cs50 import get_float

# Las monedas a usar son de .25, .10, .5 y .1 centavos
# Los comentarios los estoy copiando del cash.c del pset1 xd

while True:
    c = get_float('Cuanto cambio desea:')
    if c > 0:
        break
# Pasa el cambio de decimales a enteros
cent = c * 100
cont = 0

# Valida si la cantidad es mayor o igual a 25 para dar una moneda de 25 centavos

while cent >= 25:
    cent = cent - 25
    cont += 1

# Valida si la cantidad es mayor o igual a 10 para dar una moneda de 10 centavos

while cent >= 10:
    cent = cent - 10
    cont += 1

# Valida si la cantidad es mayor o igual a 5 para dar una moneda de 5 centavos

while cent >= 5:
    cent = cent - 5
    cont += 1

# Valida si la cantidad es mayor o igual a 1 para dar una moneda de 1 centavos

while cent >= 1:
    cent = cent - 1
    cont += 1

# Imprime el total de monedas a entregar de cambio

print(cont)