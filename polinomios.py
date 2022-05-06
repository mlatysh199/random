# Maximilian Latysh
# 2022

import sys
# Infinito.
oo = (1 << 31) - 1
# Manejo de recursión en python.
sys.setrecursionlimit(oo)
# Factor de error.
error = 0.001


# Explicación: Encuentra todos los factores de un número (para el teorema del factor).
# Dominio: Un número entero.
# Codominio: Un arreglo de naturales.
def factores(n):
	n = abs(n)
	return [i for i in range(1, (n >> 1) + 1) if not n % i] + [n]


# Explicación: Eleva un número a otro.
# Dominio: Un número racional (x) y un número natural (n).
# Codominio: Los números racionales.
def elevar(x, n):
	mult = 1
	for i in range(n):
		mult *= x
	return mult


# Explicación: Encuentra el valor de P(x)
# Dominio: Un arreglo de enteros y un número racional.
# Codominio: Los números racionales.
def caracterizar(polinomio, x):
	suma = 0
	for i in range(len(polinomio)):
		suma += polinomio[len(polinomio) - i - 1]*elevar(x, i)
	return suma


# Explicación: Utiliza el teorema de los factores racionales para encontrar
# - los factores racionales de un polinomio.
# Dominio: Un arreglo de enteros.
# Codominio: Un arreglo de racionales.
def cerosRacionales(polinomio):
	soluciones = []
	posibilidades = set()
	for q in factores(polinomio[0]):
		for p in factores(polinomio[-1]):
			posibilidades.add(p/q)
	for i in posibilidades:
		a, b = caracterizar(polinomio, i), caracterizar(polinomio, -i)
		soluciones += [i]*(a - error <= 0 <= a + error) + [-i]*(b - error <= 0 <= b + error)
	return soluciones


# Explicación: Encuentra la derivada de un polinomio.
# Dominio: Un arreglo de enteros.
# Codominio: Un arreglo de enteros.
def derivar(polinomio):
	nuevo = []
	for i in range(1, len(polinomio)):
		nuevo = [polinomio[len(polinomio) - i - 1]*(i)] + nuevo
	return nuevo


# Explicación: Insertion Sort con BB.
# Dominio: Un punto cartesiano y una lista de dichos puntos.
# Codiminio: Vacío (cambia la lista en sí).
def meter(punto, monotonia):
	inf = 0
	sup = len(monotonia)
	if not sup:
		monotonia.append(punto)
		return
	mid = (inf + sup) >> 1
	while inf != mid:
		if monotonia[mid][0] > punto[0]:
			inf = mid
		elif monotonia[mid][0] < punto[0]:
			sup = mid
		else:
			monotonia.insert(mid, punto)
		mid = (inf + sup) >> 1
	if monotonia[mid][0] >= punto[0]:
		monotonia.insert(mid, punto)
		return
	monotonia.insert(mid + 1, punto)


# Explicación: Encuentra el cero entre dos puntos utilizando BB.
# Dominio: Una lista con un par de puntos cartesianos, una lista de enteros,
# - un arreglo de racionales.
def entreMonotonias(intervalos, polinomio, soluciones):
	for i in intervalos:
		sup = i[1][0]
		inf = i[0][0]
		pendiente = i[0][1] < i[1][1]
		mid = (inf + sup)/2
		intento = caracterizar(polinomio, mid)
		while not (intento - error <= 0 <= intento + error):
			intento = intento > 0
			if intento and pendiente or not intento and not pendiente:
				sup = mid
			else:
				inf = mid
			mid = (inf + sup)/2
			intento = caracterizar(polinomio, mid)
		soluciones.append(mid)


# ----- MAIN -----
# Explicación: Encuentra las soluciones de un polinomio.
# Dominio: Arreglo de enteros.
# Codominio: Bit de validez con el conjunto de racionales.
# Se retornan dos valores. Verdad o falso dependiendo de que si hay soluciones
# - y las soluciones. Si las soluciones son infinitas, se retorna (True, [])
# Se asume que el primer valor de la lista no es 0.
def solucionesPolinomio(polinomio):
	# Primera parte: Intentamos encontrar todos los factores racionales.
	# Simplificación del polinomio.
	soluciones = []
	if len(polinomio) == 1:
		if not polinomio[-1]:
			return True, []
		return False, []
	if not polinomio[-1]:
		soluciones.append(0)
	while not polinomio[-1]:
		polinomio.pop()
	if len(polinomio) == 1:
		return True, soluciones
	# Teorema de los ceros racionales
	soluciones += cerosRacionales(polinomio)
	# Si ya hemos encontrado la máxima cantidad de factores, hemos terminado!
	if len(soluciones) == len(polinomio) - 1:
		return True, soluciones
	# No encontramos factores racionales. Por lo tanto, vamos a hacer un
	# - procedimiento malvado. Vamos a calcular las posiciones en las cuales
	# - la monotonía llega a ser 0. Esto lo hacemos recursivamente encontrando
	# - la derivada del polinomio, encontrando las soluciones de la derivada,
	# - sacando la segunda derivada si la primera no tenía soluciones racionales
	# - y así en adelante hasta que la derivada toma la forma ax + b. En este
	# - caso, ya sabemos que va a tener un factor racional.
	# Volviendo, sabemos que si dos cambios de monotonía seguidos tienen signos
	# - diferentes (en referencia con la eje x), sabemos que existe un 0 en el
	# - intervalo dado. Un cambio de monotonía es justamente un 0, lo agregamos
	# - como una solución y lo ignoramos para el proceso anterior.
	monotonia = []
	soluciones = [0]*(0 in soluciones)
	# Encontramos los puntos de cambio de monotonía.
	for i in solucionesPolinomio(derivar(polinomio))[1]:
		intento = caracterizar(polinomio, i)
		magia = False
		if intento - error <= 0 <= intento + error:
			magia = True
			soluciones.append(intento)
		meter([i, intento, magia], monotonia)
	monotonia = [[-oo, oo*(1 - 2*(not len(polinomio)&1))*(1 - 2*(polinomio[0] < 0)), False]] + monotonia + [[oo, oo*(1 - 2*(polinomio[0] < 0)), False]]
	intervalos = []
	previo = monotonia[0]
	# Creamos los intervalos entre cambios de monotonía.
	for i in range(1, len(monotonia)):
		if not previo[2] and not monotonia[i][2]:
			if not ((previo[1] > 0) == (monotonia[i][1] > 0)):
				intervalos.append([previo, monotonia[i]])
		previo = monotonia[i]
	entreMonotonias(intervalos, polinomio, soluciones)
	return True, soluciones


# Para hacer pruebas
if __name__ == "__main__":
	print(solucionesPolinomio([20, 77, 41, -30]))
	print(solucionesPolinomio([3, 2, 6, 2]))
	print(solucionesPolinomio([3]))
	print(solucionesPolinomio([0]))
	print(solucionesPolinomio([6, 0, 0, 3, -9, 0, 0, 0]))
	print(solucionesPolinomio([1, 0, 1, 7, 0, 7, 0]))
	print(solucionesPolinomio([-6, -11, 0, 18, 33]))
