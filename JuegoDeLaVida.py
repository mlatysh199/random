import curses


def terminar(p):
	curses.nocbreak()
	p.keypad(False)
	curses.echo()
	curses.endwin()
	quit()


def crearMatrizVacia(filas, columnas):  # Esta funcion se encarga de crear una matriz vacia de nxm dimensiones
    matriz_nueva = [[0]] * filas  # Como el vacio en este proyecto se representa con "." la matriz vacia se llena de este simbolo
    for posFila in range(filas):
        matriz_nueva[posFila] = matriz_nueva[posFila]*columnas
    return matriz_nueva


def esvalido(filas, cols, posI, posJ):  # Esta funcion se encarga de ver si existe una posicion en la matriz
    return 0 <= posI <= filas and 0 <= posJ <= cols


direcciones = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [0, -1], [1, -1], [1, 0], [1, 1]]
def jugar(matriz):
    columnas = len(matriz[0])
    filas = len(matriz)
    herencia = crearMatrizVacia(filas,columnas)
    for i in range(filas):
        for j in range(columnas):
            cuentavivas = 0
            for k in range(len(direcciones)):
                nuevoi = i + direcciones[k][0]
                nuevoj = j + direcciones[k][1]
                if esvalido(filas - 1, columnas - 1, nuevoi, nuevoj):
                    if matriz[nuevoi][nuevoj]:
                        cuentavivas += 1
            if matriz[i][j]:
                if cuentavivas == 3 or cuentavivas == 2:
                    herencia[i][j] = True
            if not matriz[i][j]:
                if cuentavivas == 3:
                    herencia[i][j] = True
    return herencia


def pantalla(s):	
	curses.start_color()
	curses.cbreak()
	curses.noecho()
	s.nodelay(True)
	estado, correr = True, True
	largo, ancho = 40, 80
	p = curses.newwin(largo, ancho, 0, 0)
	p.timeout(200)
	p.keypad(True)
	curses.curs_set(False)
	p.border(0)
	print("\x1b[8;40;80t")
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLUE)
	matriz = [[False]*(ancho - 2) for i in range(largo - 2 - 6)]
	cursor = [0, 0]
	while correr:
		c = s.getch()
		p.erase()
		p.border(0)
		for i in range(1, ancho - 1):
			p.addch(6, i, "-")
		for i in range(0, largo - 2 - 6):
			for j in range(0, ancho - 2):
				b = curses.color_pair(1) if matriz[i][j] else curses.color_pair(2)
				p.addch(i + 7, j + 1, "█", b)
		if estado:
			if c == curses.KEY_LEFT and cursor[1] > 0:
				cursor[1] -= 1
			elif c == curses.KEY_RIGHT and cursor[1] < ancho - 3:
				cursor[1] += 1
			elif c == curses.KEY_UP and cursor[0] > 0:
				cursor[0] -= 1
			elif c == curses.KEY_DOWN and cursor[0] < largo - 2 - 6 - 1:
				cursor[0] += 1
			p.addch(7 + cursor[0], 1 + cursor[1], "X", curses.color_pair(3))
			if c == 10:
				matriz[cursor[0]][cursor[1]] = not matriz[cursor[0]][cursor[1]]
		else:
			matriz = jugar(matriz)
		p.addstr(1, (ancho>>1)-9, "EL JUEGO DE LA VIDA", curses.color_pair(4))
		p.addstr(2, 2, "CONTROLES:", curses.color_pair(4))
		p.addstr(4, ancho - 25, "q -> para salir", curses.color_pair(4))
		p.addstr(4, 5, "p -> para activar o desactivar el juego", curses.color_pair(4))
		p.addstr(5, 5, "b -> para borrar el juego", curses.color_pair(4))
		p.addstr(3, 5, "INTRO -> para cambiar el estado de la celda o para acelerar la simulación", curses.color_pair(4))
		p.addstr(5, (ancho>>1), "FLECHAS -> para mover el cursor", curses.color_pair(4))
		if c == ord("q"):
			terminar(p)
		if c == ord("p"):
			estado = not estado
		if c == ord("b"):
			matriz = [[False]*(ancho - 2) for i in range(largo - 2 - 6)]
		if not estado and c != 10:
			curses.napms(300)
		p.refresh()


if __name__ == "__main__":
	curses.wrapper(pantalla)  # (curses.initscr())
