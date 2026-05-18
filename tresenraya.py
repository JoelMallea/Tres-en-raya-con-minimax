import math
import tkinter as tk
import copy

# =============================================================================
# CONFIGURACIÓN E INICIALIZACIÓN DE VARIABLES GLOBALES
# =============================================================================
# Definimos constantes para representar los estados de las casillas y los jugadores.
# Esto evita errores de tipeo a lo largo del código.
X = "X"          # Humano (Maximizador)
O = "O"          # Inteligencia Artificial (Minimizador)
EMPTY = None    # Casilla vacía

# =============================================================================
# MÉTODOS DE ABSTRACCIÓN DEL JUEGO (Estructura estándar para IA)
# =============================================================================

def initial_state():
    """
    Genera y retorna la estructura de datos inicial para el juego.
    Representamos el tablero como una matriz bidimensional (lista de listas) de 3x3
    inicializada completamente con valores vacíos (None).
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Determina de quién es el turno actual analizando el estado del tablero.
    Contamos cuántas jugadas ha realizado cada símbolo. Dado que 'X' siempre
    inicia la partida, si el número de 'X' es igual al de 'O', significa que
    corresponde el turno de 'X'. De lo contrario, le toca a 'O'.
    """
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)
    
    if count_x > count_o:
        return O
    else:
        return X


def actions(board):
    """
    Explora el tablero y devuelve un conjunto (set) con todas las acciones legales.
    Cada acción válida se representa como una tupla de coordenadas (i, j) que 
    corresponde a una casilla que aún permanece con el estado EMPTY.
    """
    posibles_acciones = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                posibles_acciones.add((i, j))
    return posibles_acciones


def result(board, action):
    """
    Aplica una acción sobre el tablero y retorna el nuevo estado resultante.
    Para cumplir con los principios de programación funcional e inmutabilidad necesarios
    en algoritmos de búsqueda, realizamos una copia profunda (deepcopy) del tablero original.
    Esto permite simular jugadas futuras en el árbol Minimax sin alterar la partida real.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Error: La casilla seleccionada ya está ocupada.")
    
    nuevo_tablero = copy.deepcopy(board)
    nuevo_tablero[i][j] = player(board) # Asigna el símbolo del jugador en turno
    return nuevo_tablero


def winner(board):
    """
    Analiza el tablero actual para verificar si existe una condición de victoria.
    Evalúa secuencialmente las 3 filas, las 3 columnas y las 2 diagonales principales.
    Si encuentra tres símbolos idénticos alineados (y diferentes de None), retorna dicho símbolo.
    Si no hay ningún ganador, devuelve None.
    """
    # Verificación de alineaciones horizontales (Filas)
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
            
    # Verificación de alineaciones verticales (Columnas)
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return board[0][j]
            
    # Verificación de la diagonal principal (\)
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
        
    # Verificación de la diagonal secundaria (/)
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
        
    return None


def terminal(board):
    """
    Evalúa si la partida actual ha llegado a su fin (Caso Base del árbol de decisión).
    El juego se considera terminado bajo dos condiciones: 
    1. Ya existe un ganador definitivo en el tablero.
    2. El tablero está completamente lleno (empate), por lo que no quedan movimientos posibles.
    """
    if winner(board) is not None:
        return True
        
    for row in board:
        if EMPTY in row:
            return False # Todavía quedan casillas vacías y nadie ha ganado
            
    return True


def utility(board):
    """
    Asigna un valor numérico final a los estados terminales del juego (Función de Utilidad).
    Mapea el resultado bajo el siguiente criterio estándar de teoría de juegos:
    * Retorna  1: Si gana el jugador X (Maximizador).
    * Retorna -1: Si gana el jugador O (Minimizador / IA).
    * Retorna  0: Si la partida finaliza en empate (Nadie gana).
    """
    ganador = winner(board)
    if ganador == X:
        return 1
    elif ganador == O:
        return -1
    else:
        return 0


# =============================================================================
# IMPLEMENTACIÓN DEL ALGORITMO MINIMAX
# =============================================================================

def minimax(board):
    """
    Función principal del algoritmo Minimax para calcular la jugada óptima.
    Analiza de quién es el turno y recorre todas las acciones disponibles, evaluando 
    el árbol de decisiones de manera recursiva para seleccionar el movimiento que 
    garantice el mejor resultado matemático posible contra un oponente perfecto.
    """
    if terminal(board):
        return None

    turno_actual = player(board)

    # Lógica para el turno de X (Maximizar la puntuación hacia 1)
    if turno_actual == X:
        mejor_valor = -math.inf
        mejor_accion = None
        for accion in actions(board):
            valor = min_value(result(board, accion))
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_accion = accion
        return mejor_accion

    # Lógica para el turno de O / IA (Minimizar la puntuación hacia -1)
    else:
        mejor_valor = math.inf
        mejor_accion = None
        for accion in actions(board):
            valor = max_value(result(board, accion))
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_accion = accion
        return mejor_accion


def max_value(board):
    """
    Función recursiva que simula el razonamiento del jugador Maximizador (X).
    Busca maximizar la utilidad del juego eligiendo el valor más alto devuelto
    por las respuestas del oponente (min_value).
    """
    if terminal(board):
        return utility(board)
    v = -math.inf
    for accion in actions(board):
        v = max(v, min_value(result(board, accion)))
    return v


def min_value(board):
    """
    Función recursiva que simula el razonamiento del jugador Minimizador (O).
    Busca minimizar la utilidad del juego seleccionando el valor más bajo posible
    frente a las jugadas óptimas simuladas para el jugador humano (max_value).
    """
    if terminal(board):
        return utility(board)
    v = math.inf
    for accion in actions(board):
        v = min(v, max_value(result(board, accion)))
    return v


# =============================================================================
# CAPA DE INTERFAZ GRÁFICA DE USUARIO (GUI con Tkinter)
# =============================================================================

class JuegoTresEnRaya:
    def __init__(self, ventana):
        """
        Constructor de la interfaz gráfica. Inicializa la ventana principal,
        asigna los estados del tablero lógico y construye los componentes visuales.
        """
        self.ventana = ventana
        self.ventana.title("Tres en Raya - Inteligencia Artificial")
        
        self.tablero = initial_state()
        self.botones = [[None for _ in range(3)] for _ in range(3)]
        
        # Etiqueta de texto superior para informar el estado y turnos en tiempo real
        self.texto_estado = tk.Label(self.ventana, text="Tu turno (Juegas con X)", font=('Arial', 14, 'bold'), pady=10)
        self.texto_estado.grid(row=0, column=0, columnspan=3)
        
        # Inicialización y posicionamiento de la matriz de botones 3x3
        for i in range(3):
            for j in range(3):
                # Usamos una función lambda para pasar las coordenadas específicas de cada botón al hacer clic
                btn = tk.Button(self.ventana, text="", font=('Arial', 20, 'bold'), width=5, height=2,
                                bg="#ededed", command=lambda r=i, c=j: self.jugar(r, c))
                btn.grid(row=i+1, column=j, padx=4, pady=4)
                self.botones[i][j] = btn
                
        # Botón inferior para restablecer la partida de forma ágil y directa
        btn_reiniciar = tk.Button(self.ventana, text="Reiniciar Juego", font=('Arial', 11), bg="#d9534f", fg="white", command=self.reiniciar)
        btn_reiniciar.grid(row=4, column=0, columnspan=3, sticky="we", padx=10, pady=12)


    def jugar(self, i, j):
        """
        Controlador de eventos para gestionar los turnos tras el clic del usuario.
        Ejecuta el movimiento humano, actualiza la GUI, verifica si finalizó el juego,
        y si la partida continúa, invoca de inmediato el cálculo de Minimax para la IA.
        """
        # Control de seguridad: Si la casilla ya tiene datos o el juego terminó, ignora el clic
        if terminal(self.tablero) or self.tablero[i][j] != EMPTY:
            return
        
        # 1. Procesar movimiento del Jugador Humano (Siempre asignado a X)
        self.tablero = result(self.tablero, (i, j))
        self.actualizar_interfaz()
        
        # =====================================================================
        # TRUCO DE OPTIMIZACIÓN VISUAL:
        # Forzamos a Tkinter a refrescar la pantalla e imprimir la "X" del usuario
        # ANTES de que el algoritmo Minimax sature el procesador con sus cálculos.
        # =====================================================================
        self.ventana.update_idletasks() 
        
        if self.evaluar_fin_juego():
            return # Detiene el flujo si el jugador bloqueó el tablero o ganó
        
        # 2. Procesar movimiento de la Inteligencia Artificial (Siempre asignado a O)
        accion_ia = minimax(self.tablero)
        if accion_ia is not None:
            self.tablero = result(self.tablero, accion_ia)
            self.actualizar_interfaz()
            self.evaluar_fin_juego()


    def actualizar_interfaz(self):
        """
        Sincroniza la lógica de la matriz bidimensional interna con la interfaz gráfica.
        Cambia el texto expuesto en los botones y modifica sus colores de fondo para 
        mejorar la experiencia visual y diferenciar claramente a los jugadores.
        """
        for i in range(3):
            for j in range(3):
                valor = self.tablero[i][j]
                texto = valor if valor is not None else ""
                
                # Renderizado de colores según el jugador
                if valor == X:
                    color_fondo = "#337ab7" # Azul para el Humano
                    color_texto = "white"
                elif valor == O:
                    color_fondo = "#d42727" # Rojo para la IA
                    color_texto = "white"
                else:
                    color_fondo = "#ededed" # Gris por defecto (Vacío)
                    color_texto = "black"
                
                self.botones[i][j].config(text=texto, bg=color_fondo, fg=color_texto)


    def evaluar_fin_juego(self):
        """
        Comprueba el estado del juego para actualizar la etiqueta informativa principal.
        Si la función terminal() retorna True, bloquea el flujo de juego actual y 
        escribe de manera directa el desenlace en la pantalla sin usar diálogos emergentes.
        """
        if terminal(self.tablero):
            resultado = winner(self.tablero)
            if resultado == X:
                self.texto_estado.config(text="¡Ganaste el juego!")
            elif resultado == O:
                self.texto_estado.config(text="La IA ha ganado.")
            else:
                self.texto_estado.config(text="Empate: Nadie gana.")
            return True
            
        # Si el juego continúa, refresca el mensaje indicando a quién le toca mover
        siguiente = player(self.tablero)
        if siguiente == X:
            self.texto_estado.config(text="Tu turno (Juegas con X)")
        else:
            self.texto_estado.config(text="Turno de la IA...")
        return False


    def reiniciar(self):
        """
        Restablece por completo la lógica interna y limpia los componentes visuales de la interfaz
        para permitir al usuario iniciar una nueva partida sin necesidad de reiniciar el script.
        """
        self.tablero = initial_state()
        self.actualizar_interfaz()
        self.texto_estado.config(text="Tu turno (Juegas con X)")


# =============================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoTresEnRaya(root)
    root.mainloop() # Inicia el bucle de escucha de eventos de Tkinter