# Rubik-s-Race

### Miembros - Grupo 1:
Yazmina Yepes, 
Luisangel Parra, 
Jorge Peña

![image](https://github.com/user-attachments/assets/0ab43c75-2fbf-4a0a-8bde-ea96ec466bc0)

### **Documentación del Examen y Solución Implementada** 📚

---

## **Descripción del Examen** 📝

El examen consiste en implementar un algoritmo de **Búsqueda A*** en Python para resolver un juego de **Rubik’s Race**. El objetivo es encontrar una solución que permita pasar de un **estado inicial** a un **estado meta**, ambos definidos en archivos de texto (`.txt`). Cada casilla del tablero se representa con los siguientes colores:

- `*`: Casilla vacía.
- `B`: Blanco.
- `R`: Rojo.
- `V`: Verde.
- `N`: Naranja.
- `Z`: Azul.
- `A`: Amarillo.

### **Características del Examen** 🎯

1. **Implementación en Python**:
   - El código debe estar escrito en Python.
   - Se debe usar **Jupyter Notebook** para integrar el reporte con la implementación.

2. **Movimientos Permitidos**:
   - **Arriba (1)**: La ficha debajo de la casilla vacía se mueve hacia arriba.
   - **Abajo (2)**: La ficha arriba de la casilla vacía se mueve hacia abajo.
   - **Izquierda (3)**: La ficha a la derecha de la casilla vacía se mueve hacia la izquierda.
   - **Derecha (4)**: La ficha a la izquierda de la casilla vacía se mueve hacia la derecha.

3. **Archivo de Salida**:
   - Se debe generar un archivo de texto (`.txt`) que contenga:
     - La heurística de cada movimiento.
     - El movimiento seleccionado.
     - El estado del juego después de aplicar el movimiento.

4. **Mensaje Final**:
   - Si se encuentra la solución, se debe mostrar un mensaje indicando que se llegó a la meta.
   - Si no hay solución, se debe indicar que el juego no tiene solución.

5. **Fecha de Entrega**:
   - Viernes 28 de Febrero de 2025, antes de las 11:59 p.m.

---

## **Desarrollo de la Solución** 🛠️

### **1. Lector de Archivos** 📂

El código comienza con la función `read_input_file`, que se encarga de leer el archivo de texto que contiene el estado del tablero.

```python
def read_input_file(file_name):
    """
    Lee un archivo de texto que representa el estado del tablero y lo convierte en una lista de listas.

    Parámetros:
        file_name (str): Nombre del archivo que contiene el estado del tablero.

    Retorna:
        list: Una lista de listas que representa el estado del tablero.
    """
    file_path = os.path.join(file_name)  # Obtiene la ruta completa del archivo.
    with open(file_path, 'r') as file:   # Abre el archivo en modo lectura.
        # Lee cada línea del archivo, elimina espacios en blanco y la convierte en una lista de caracteres.
        state = [list(line.strip()) for line in file]
    file.close()  # Cierra el archivo después de leerlo.
    return state  # Devuelve el estado del tablero como una lista de listas.
```

#### **Explicación**:
- **Entrada**: El nombre del archivo (`file_name`).
- **Salida**: Una lista de listas que representa el estado del tablero.
- **Proceso**:
  - Abre el archivo en modo lectura.
  - Lee cada línea, elimina espacios en blanco y la convierte en una lista de caracteres.
  - Cierra el archivo y devuelve el estado del tablero.

---

### **2. Clase `PuzzleState`** 🧩

Esta clase representa un estado del rompecabezas, incluyendo el tablero, el estado padre, el movimiento realizado, la profundidad en el árbol de búsqueda y el costo total.

```python
class PuzzleState:
    """
    Representa un estado del rompecabezas, incluyendo el tablero, el estado padre, el movimiento realizado,
    la profundidad en el árbol de búsqueda y el costo total (profundidad + heurística).
    """
    def __init__(self, board, parent, move, depth, cost):
        self.board = board  # Configuración del tablero.
        self.parent = parent  # Estado padre en el árbol de búsqueda.
        self.move = move  # Movimiento realizado para llegar a este estado.
        self.depth = depth  # Profundidad en el árbol de búsqueda.
        self.cost = cost  # Costo total (profundidad + heurística).

    def __lt__(self, other):
        """
        Método para comparar dos estados basado en su costo.
        Se utiliza para ordenar los estados en la cola de prioridad.
        """
        return self.cost < other.cost
```

#### **Explicación**:
- **Atributos**:
  - `board`: Representa el estado actual del tablero.
  - `parent`: Estado padre en el árbol de búsqueda.
  - `move`: Movimiento realizado para llegar a este estado.
  - `depth`: Profundidad en el árbol de búsqueda.
  - `cost`: Costo total (profundidad + heurística).
- **Método `__lt__`**: Compara dos estados basado en su costo. Se utiliza para ordenar los estados en la cola de prioridad.

---

### **3. Validación del Estado del Tablero** ✅

La función `validate_file_state` valida que el estado del tablero cumpla con las reglas del problema.

```python
def validate_file_state(file_state, goal, min_size=3):
    """
    Valida que el estado del tablero cumpla con las reglas del problema.

    Parámetros:
        file_state (list): Estado del tablero como lista de listas.
        goal (bool): Indica si el estado es el estado meta.
        min_size (int): Tamaño mínimo del tablero.

    Lanza:
        ValueError: Si el tablero no cumple con las reglas.
    """
    # Verifica que el tablero tenga al menos 3 filas y 3 columnas.
    if len(file_state) < min_size or any(len(row) < min_size for row in file_state):
        raise ValueError(f'The board must have at least {min_size}x{min_size} dimensions')

    # Verifica que solo contenga colores válidos.
    colors = set(flatten(file_state))  # Obtiene todos los colores en el tablero.
    invalid_colors = colors - set(color_abbreviation.keys())  # Encuentra colores no válidos.
    if invalid_colors:
        raise ValueError(f'Invalid colors found: {invalid_colors}, must be one of {color_abbreviation.keys()}')

    if goal == False:
        # Verifica la cantidad de bloques de cada color.
        n = len(file_state)  # Tamaño del tablero.
        total_blocks = n * n  # Total de bloques en el tablero.
        colors = ['V', 'B', 'R', 'A', 'N', 'Z']  # Colores válidos.
        blocks_per_color = (total_blocks - 1) // 6  # Cantidad esperada de bloques por color.

        # Diccionario con la cantidad esperada de cada color.
        expected_counts = {color: blocks_per_color for color in colors}
        expected_counts['*'] = 1  # Solo debe haber un bloque negro.

        # Cuenta la cantidad real de bloques de cada color.
        actual_counts = Counter(color for row in file_state for color in row)

        # Encuentra diferencias entre la cantidad esperada y la real.
        invalid_counts = {color: actual_counts.get(color, 0) - expected_counts.get(color, 0)
                          for color in expected_counts if actual_counts.get(color, 0) != expected_counts.get(color, 0)}

        if invalid_counts:
            raise ValueError(f'Invalid color count. Must have {blocks_per_color} blocks per color, and 1 black block.')
```

#### **Explicación**:
- **Validaciones**:
  - El tablero debe tener al menos 3 filas y 3 columnas.
  - Solo se permiten colores válidos.
  - La cantidad de bloques de cada color debe ser correcta.

---

### **4. Generación de Estados Inicial y Meta** 🎲

Las funciones `generate_initial_state_from_file` y `generate_goal_state_from_file` generan los estados inicial y meta a partir de los archivos de texto.

```python
def generate_initial_state_from_file(file_name, goal=False):
    """
    Genera el estado inicial del rompecabezas a partir de un archivo.

    Parámetros:
        file_name (str): Nombre del archivo que contiene el estado inicial.
        goal (bool): Indica si el estado es el estado meta.

    Retorna:
        list: Estado inicial como una lista aplanada.
    """
    file_state = read_input_file(file_name)  # Lee el archivo.
    try:
        validate_file_state(file_state, goal)  # Valida el estado.
    except ValueError as e:
        print(e)
        exit(1)

    # Convierte el estado en una lista aplanada.
    grid = [[[color for color in row] for row in file_state]]
    initial_state = flatten(flatten(grid))
    return initial_state
```

#### **Explicación**:
- **Entrada**: Nombre del archivo y un indicador de si es el estado meta.
- **Salida**: Estado inicial o meta como una lista aplanada.
- **Proceso**:
  - Lee el archivo.
  - Valida el estado.
  - Convierte el estado en una lista aplanada.

---

### **5. Heurística Adaptada** 🧠

La heurística utilizada es una variante de la **distancia Manhattan**, que calcula la distancia mínima desde un punto de referencia en la solución hacia los colores en el tablero actual.

```python
def heuristic(board):
    """
    Calcula la heurística (distancia Manhattan adaptada) para un estado dado.

    Parámetros:
        board (list): Estado del tablero como una lista aplanada.

    Retorna:
        int: Valor heurístico.
    """
    total_distance = 0
    for i, color in enumerate(board):
        for y, x in [divmod(i, 5)]:  # Convierte el índice en coordenadas (fila, columna).
            if i in i_3x3:  # Solo considera la región central de 3x3.
                if board[i] != '*' and goal_postions[color]:
                    # Calcula la distancia mínima desde el punto de referencia a los colores.
                    total_distance += min(manhattan_distance((y, x), pos) for pos in goal_postions[color])
                if color != goal_state[(y - 1) * 3 + (x - 1)]:
                    total_distance += 1  # Penaliza si el color no está en la posición correcta.
    return total_distance
```

#### **Explicación**:
- **Entrada**: Estado del tablero como una lista aplanada.
- **Salida**: Valor heurístico.
- **Proceso**:
  - Calcula la distancia Manhattan desde un punto de referencia en la solución hacia los colores en el tablero actual.
  - Suma las distancias mínimas para obtener el valor heurístico total.

---

### **6. Algoritmo A*** 🔍

El algoritmo A* se implementa en la función `a_star`, que busca la solución óptima utilizando una cola de prioridad.

```python
def a_star(start_state, goal_state):
    """
    Implementa el algoritmo A* para encontrar la solución al rompecabezas.

    Parámetros:
        start_state (list): Estado inicial del tablero.
        goal_state (list): Estado meta del tablero.

    Retorna:
        PuzzleState: Estado final que representa la solución, o None si no se encuentra.
    """
    open_list = []  # Lista de estados por explorar.
    closed_list = set()  # Lista de estados ya explorados.
    # Inicia con el estado inicial.
    heapq.heappush(open_list, PuzzleState(start_state, None, None, 0, heuristic(start_state)))

    while open_list:
        current_state = heapq.heappop(open_list)  # Extrae el estado con menor costo.
        current_state_goal_positions = [current_state.board[i] for i in i_3x3]

        # Si el estado actual es el objetivo, devuelve la solución.
        if current_state_goal_positions == goal_state:
            return current_state

        closed_list.add(tuple(current_state.board))  # Marca el estado como explorado.

        blank_pos = current_state.board.index("*")  # Encuentra la posición del espacio vacío.

        # Genera nuevos estados aplicando movimientos válidos.
        for move in moves:
            if move == 'D' and blank_pos < 5:  # Movimiento inválido hacia arriba.
                continue
            if move == 'U' and blank_pos > 19:  # Movimiento inválido hacia abajo.
                continue
            if move == 'R' and blank_pos % 5 == 0:  # Movimiento inválido hacia la izquierda.
                continue
            if move == 'L' and blank_pos % 5 == 4:  # Movimiento inválido hacia la derecha.
                continue
            new_board = move_tile(current_state.board, move, blank_pos)  # Genera un nuevo estado.

            if tuple(new_board) in closed_list:  # Si el estado ya fue explorado, lo ignora.
                continue
            # Crea un nuevo estado y lo añade a la lista de estados por explorar.
            new_state = PuzzleState(new_board, current_state, move, current_state.depth + 1, current_state.depth + 1 + heuristic(new_board))
            heapq.heappush(open_list, new_state)

    return None  # Si no se encuentra solución, devuelve None.
```

#### **Explicación**:
- **Entrada**: Estado inicial y estado meta.
- **Salida**: Estado final que representa la solución, o `None` si no se encuentra.
- **Proceso**:
  - Utiliza una cola de prioridad para explorar los estados.
  - Si el estado actual es el objetivo, devuelve la solución.
  - Genera nuevos estados aplicando movimientos válidos y los añade a la cola de prioridad.

---

### **7. Impresión de la Solución** 🖨️

La función `print_solution` imprime el camino de la solución desde el estado inicial hasta el estado meta.

```python
def print_solution(solution):
    """
    Imprime el camino de la solución desde el estado inicial hasta el estado meta.

    Parámetros:
        solution (PuzzleState): Estado final que representa la solución.
    """
    path = []
    current = solution
    while current:
        path.append(current)  # Reconstruye el camino desde el estado final hasta el inicial.
        current = current.parent
    path.reverse()  # Invierte el camino para mostrarlo en orden.

    for step in path:
        print(f"Move: {step.move}")  # Imprime el movimiento realizado.
        print_board(step.board)  # Imprime el tablero en ese paso.
```

#### **Explicación**:
- **Entrada**: Estado final que representa la solución.
- **Salida**: Impresión del camino de la solución.
- **Proceso**:
  - Reconstruye el camino desde el estado final hasta el inicial.
  - Imprime cada movimiento y el estado del tablero en ese paso.

---


### **Referencias** 📚

- [1] GeeksforGeeks, "8-Puzzle Problem in AI," GeeksforGeeks. [En línea]. Disponible: https://www.geeksforgeeks.org/8-puzzle-problem-in-ai/. [Accedido: 23 feb, 2025].

---

### **Resumen de la Lógica** 🎉

El código presentado implementa la solución al problema del rompecabezas 8-puzzle utilizando el algoritmo de búsqueda A* (A-Star), reconocido por su eficiencia en encontrar caminos óptimos en espacios de estados complejos. La solución comienza con la definición de la clase PuzzleState, que representa un estado del rompecabezas. Esta clase almacena el tablero actual, el estado padre, el movimiento realizado para alcanzar dicho estado, la profundidad en el árbol de búsqueda y el costo total, que es la suma de la profundidad y la heurística. La heurística utilizada es una variante de la distancia Manhattan, adaptada para calcular la distancia mínima desde un punto de referencia en la solución hasta las posiciones de los colores en el tablero actual.

En esta implementación, la heurística no calcula la distancia Manhattan tradicional (desde cada bloque hasta su posición objetivo). En su lugar, se toma un punto de referencia en la solución (uno de los puntos de la configuración objetivo) y se calcula la distancia Manhattan desde este punto hacia todas las casillas que contienen colores en el tablero actual. Luego, se selecciona la distancia mínima para cada color y se suman todas estas distancias mínimas para obtener el valor heurístico total. Este enfoque garantiza una estimación más precisa del costo restante para alcanzar la solución, optimizando así la búsqueda.

Para la lectura del estado inicial y el estado meta del rompecabezas, el código emplea la función read_input_file, que extrae la configuración desde archivos de texto. La validación del estado se realiza en la función validate_file_state, asegurando que el tablero tenga un tamaño mínimo de 3x3, contenga únicamente colores válidos y cumpla con la distribución esperada de colores, incluyendo exactamente un bloque negro (‘’) que representa el espacio vacío. Posteriormente, las funciones *generate_initial_state_from_file** y generate_goal_state_from_file convierten la matriz del archivo en una lista aplanada, facilitando la manipulación de estados.

Para representar los movimientos posibles del bloque vacío dentro del tablero, se define un diccionario moves, donde cada movimiento (U, D, L, R) está asociado a un desplazamiento en la lista unidimensional. La función move_tile permite generar nuevos estados aplicando un movimiento sobre el estado actual. Además, la función calculate_goal_positions mapea las posiciones objetivo de cada color dentro del tablero, lo que permite el cálculo eficiente de la heurística adaptada.

El núcleo de la solución es la función a_star, que implementa la búsqueda A* utilizando una cola de prioridad (heapq) para almacenar los estados explorados en función de su costo total. El algoritmo inicia insertando el estado inicial con su respectiva heurística. En cada iteración, se extrae el estado con menor costo de la cola de prioridad. Si el estado coincide con el objetivo, se reconstruye el camino desde el estado final hasta el inicial mediante la función print_solution, mostrando los movimientos realizados para resolver el rompecabezas. Si el estado no es el objetivo, se generan los estados sucesores aplicando los movimientos posibles y se añaden a la cola si no han sido explorados previamente.

Finalmente, el código ejecuta la generación del estado inicial y meta, los muestra visualmente en consola utilizando print_board, y ejecuta la búsqueda A* para encontrar la solución. Si se encuentra una solución, se imprime el camino óptimo; en caso contrario, se notifica que no existe solución. Esta implementación combina estructuras de datos eficientes con una heurística adaptada y optimizada, garantizando una búsqueda óptima en el espacio de estados del 8-puzzle.
