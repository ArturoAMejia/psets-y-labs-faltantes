from cs50 import get_int

while True:
    a = get_int('altura: ')
    # Válida si la altura ingresada es menor que 0 o si es mayor que 23
    if 0 <= a <= 23:
        break

i = 1

# Bucle que imprime los hashes
for i in range(a):
    # Bucle que se encarga de desplegar los espacios necesarios
    for espacios in range(1, a-i, 1):
        print(' ', end="")
    for j in range(i + 2):
        print('#', end="")

    print()