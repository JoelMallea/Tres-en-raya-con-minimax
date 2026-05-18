# Juego de Tres en Raya (Tic-Tac-Toe) con Algoritmo Minimax

Este repositorio contiene la implementación completa del clásico juego **Tres en Raya** desarrollado en Python. El proyecto combina una interfaz gráfica de usuario (GUI) interactiva con un motor de Inteligencia Artificial basado en el algoritmo de búsqueda exhaustiva **Minimax**, garantizando una estrategia de juego perfecta contra el usuario.

El diseño del software sigue un enfoque modular, separando estrictamente las reglas lógicas y matemáticas del juego de la capa de presentación visual.

---

## 🧠 Arquitectura de Inteligencia Artificial

Para el modelado del juego como un problema de búsqueda en el espacio de estados, se implementaron de forma rigurosa los métodos estándar de la teoría de juegos e IA:

*   **`initial_state()`**: Define el estado inicial del problema mediante una matriz bidimensional de $3 \times 3$ inicializada en valores nulos (`None`).
*   **`player(board)`**: Evalúa de manera dinámica el turno del jugador actual mediante el conteo de elementos en la matriz, determinando si corresponde el movimiento a **X** o a **O**.
*   **`actions(board)`**: Explora el espacio de búsqueda para compilar un conjunto (`set`) de tuplas discretas `(i, j)` que representan todas las transiciones válidas disponibles.
*   **`result(board, action)`**: Aplica de forma determinista una acción sobre el tablero. Utiliza **copias profundas (`copy.deepcopy`)** para preservar el principio de inmutabilidad, permitiendo la exploración de nodos del árbol sin corromper el estado actual de la partida.
*   **`terminal(board)`**: Actúa como el caso base de la recursión, verificando si el tablero cumple con los criterios de parada (victoria, derrota o saturación de casillas).
*   **`utility(board)`**: Define la función de pago numérico o recompensa final en los nodos hoja bajó el siguiente criterio de optimización:
    *   **$1$**: Si el escenario favorece la victoria de **X** (Jugador Maximizador / Humano).
    *   **$0$**: Si el escenario concluye en un empate estructural.
    *   **$-1$**: Si el escenario favorece la victoria de **O** (Jugador Minimizador / IA).

---

## 🛠️ Funcionamiento del Motor Minimax

El algoritmo de toma de decisiones calcula la jugada óptima simulando el árbol completo de posibilidades futuras de manera recursiva. 



Cuando es el turno de la IA, el sistema asume que el usuario jugará de forma perfecta intentando maximizar su puntuación ($1$), por lo que el algoritmo selecciona la rama de decisiones que **minimice de forma absoluta** la utilidad del oponente (buscando aproximarse al $-1$). Dada la naturaleza acotada del Tres en Raya (un espacio de estados relativamente pequeño), el algoritmo calcula todas las combinaciones en milisegundos, volviéndose completamente invencible.

---

## 🎨 Componentes de la Interfaz Gráfica (GUI)

La capa visual está construida utilizando el framework nativo **Tkinter**, encapsulada bajo la clase `JuegoTresEnRaya`. 

### Optimización de Concurrencia Visual
Las interfaces gráficas nativas operan habitualmente sobre un único hilo de ejecución primario (*Main Loop*). Al calcular árboles de decisión complejos en el primer turno, el hilo de dibujo puede experimentar retrasos menores. 

Para solucionar esto de manera profesional, el software incorpora la instrucción técnica `self.ventana.update_idletasks()`. Esto fuerza el renderizado inmediato y asíncrono de la jugada del usuario antes de derivar la prioridad del procesador a las operaciones lógicas de la IA, logrando una experiencia de usuario (UX) interactiva, fluida y reactiva.

---

## 🚀 Requisitos e Instalación

Al emplear exclusivamente componentes de la biblioteca estándar de Python, el proyecto no posee dependencias de terceros, lo que asegura su portabilidad.

### 1. Clonar el repositorio localmente
```bash
git clone [https://github.com/JoelMallea/Tres-en-raya-con-minimax.git](https://github.com/JoelMallea/Tres-en-raya-con-minimax.git)
cd Tres-en-raya-con-minimax
