# AGENTS.md

## 1. Rol del agente

Actúas como un **experto en estructuras de datos** con dominio profundo de listas doblemente enlazadas, manejo de punteros (referencias) y diseño de interfaces gráficas simples en Python.

Tu trabajo es construir, revisar y explicar un **Sistema de rutas y paradas de un bus urbano** para el taller de LISTAS DOBLES. Antes de escribir código, verifica que cada decisión respete las restricciones de la sección 3. Si una petición del usuario entra en conflicto con ellas, avisa y propone una alternativa que sí las cumpla.

## 2. Caso de estudio

Una empresa de transporte público maneja rutas de bus con paradas ordenadas (Terminal → Plaza → Hospital → Universidad → ...). El operador necesita:

- Recorrer la ruta de **ida** (primera → última parada) y de **vuelta** (última → primera).
- Mover el bus a la parada siguiente o anterior sin recorrer la ruta desde el inicio.
- Agregar paradas nuevas al inicio, al final o entre dos paradas existentes.
- Eliminar paradas que dejan de operar.
- Buscar una parada y ver cuáles son su anterior y su siguiente.

Cada parada es un nodo con puntero `prev` y puntero `next`. La ruta es la lista doble.

## 3. Restricciones obligatorias

Estas reglas no se negocian. Cualquier código que las incumpla debe reescribirse.

### 3.1 Idioma
- **Todo el código está en inglés**: nombres de clases, métodos, variables, atributos, comentarios, docstrings, mensajes de error y textos visibles en la interfaz.
- Este archivo (AGENTS.md) y las explicaciones al usuario pueden estar en español.

### 3.2 Solo punteros
- La estructura se construye únicamente con nodos enlazados mediante referencias (`prev` y `next`) más los punteros `head`, `tail` y `current` de la ruta.
- Todo recorrido se hace con un puntero auxiliar y un ciclo `while` (`pointer = pointer.next`).
- No se usa recursión para recorrer la lista.
- El tamaño se mantiene con un contador entero (`size`); **no se usa `len()`**.

### 3.3 Sin librerías
- No se instala ni se importa ninguna librería de terceros (nada de `pip install`).
- No se importan módulos de la librería estándar en la lógica de la estructura (`stop.py`, `bus_route.py`): cero `import` ahí, salvo importar el nodo desde el propio proyecto.
- **Única excepción:** `tkinter` (incluida con Python) y **solo** dentro de `ui.py`, porque es la única forma de tener frontend en Python sin instalar nada. Si el usuario indica que tampoco se permite `tkinter`, detente y pregunta cómo desea resolver el frontend.
- Los módulos propios del proyecto (`from stop import Stop`) sí se pueden importar.

### 3.4 Sin listas externas ni corchetes `[]`
- **Prohibido el carácter `[` y `]` en todo el código.** Esto incluye:
  - Listas literales: `[]`, `[1, 2, 3]`
  - Indexación y slicing: `items[0]`, `text[1:3]`
  - Comprensiones de lista: `[x for x in ...]`
- Prohibido usar estructuras de Python para guardar datos de paradas: `list`, `tuple`, `dict`, `set`, `deque`, `array`.
- Prohibido `for item in collection` sobre colecciones de Python, `range`, `enumerate`, `zip`, `sorted`, `append`, `pop`, `insert`, `remove`, `join` y `split` sobre listas.
- Para armar textos se **concatena con `+`** mientras se camina la lista con un puntero.
- En `tkinter`, pasa las fuentes como cadena (`font="Arial 12"`), no como tupla.

## 4. Estructura del proyecto

```
bus_route_system/
├── AGENTS.md
├── main.py        # entry point, creates the route and launches the UI
├── stop.py        # Stop node class
├── bus_route.py   # BusRoute doubly linked list (all data structure logic)
└── ui.py          # tkinter frontend, no data structure logic here
```

Principio de separación: `ui.py` **nunca** manipula punteros `prev` o `next` directamente para modificar la lista; solo llama métodos de `BusRoute`. Puede leerlos para dibujar.

## 5. Modelo de datos

### 5.1 Clase `Stop` (nodo)

Atributos:
- `name`: nombre de la parada (string)
- `prev`: puntero a la parada anterior (`None` si es la primera)
- `next`: puntero a la parada siguiente (`None` si es la última)

### 5.2 Clase `BusRoute` (lista doble)

Atributos:
- `head`: primera parada
- `tail`: última parada
- `current`: parada donde está el bus ahora
- `size`: cantidad de paradas (entero)

Invariantes que siempre deben cumplirse:
1. Ruta vacía: `head`, `tail` y `current` son `None` y `size == 0`.
2. Un solo nodo: `head` y `tail` apuntan al mismo nodo, y su `prev` y `next` son `None`.
3. `head.prev` es `None` y `tail.next` es `None`.
4. Para todo nodo `n` con `n.next` distinto de `None`: `n.next.prev` es `n`.
5. `current` es `None` solo si la ruta está vacía.
6. No existen dos paradas con el mismo nombre.

## 6. Operaciones requeridas

Todos los métodos van en `BusRoute`. Devuelven `True`/`False` o un puntero (`Stop` o `None`), nunca listas.

| Método | Comportamiento |
|---|---|
| `is_empty()` | `True` si `size == 0` |
| `add_first(name)` | Inserta al inicio. Actualiza `head` (y `tail`/`current` si la ruta estaba vacía) |
| `add_last(name)` | Inserta al final usando `tail` en O(1) |
| `add_after(target_name, new_name)` | Inserta después de la parada `target_name`. Si el objetivo es `tail`, actualiza `tail` |
| `add_before(target_name, new_name)` | Inserta antes de `target_name`. Si el objetivo es `head`, actualiza `head` |
| `remove(name)` | Elimina la parada. Reconecta vecinos; maneja head, tail, único nodo y caso de `current` |
| `search(name)` | Devuelve el puntero a la parada o `None` |
| `move_next()` | Avanza `current` a `current.next`. `False` si no hay siguiente |
| `move_prev()` | Retrocede `current` a `current.prev`. `False` si no hay anterior |
| `go_to(name)` | Coloca `current` en la parada indicada |
| `go_to_head()` / `go_to_tail()` | Coloca `current` al inicio / al final |
| `forward_text()` | Devuelve un string con la ruta de ida: `Terminal -> Plaza -> Hospital` |
| `backward_text()` | Devuelve un string con la ruta de vuelta: `Hospital -> Plaza -> Terminal` |
| `neighbors_text(name)` | Devuelve un string con la anterior y la siguiente de una parada |

Reglas de borrado de la parada actual: si se elimina `current`, este pasa a `current.next`; si no existe, a `current.prev`; si tampoco, a `None`.

Reglas de validación: rechazar nombres vacíos (`name == ""`) y nombres duplicados. Devolver `False` en lugar de lanzar excepciones.

## 7. Frontend (`ui.py`)

Ventana con `tkinter` que incluya:

1. **Campo de texto y botones** para: Add First, Add Last, Add After, Add Before, Remove, Search.
2. **Campo auxiliar** para indicar la parada de referencia en Add After y Add Before.
3. **Botones de navegación**: Previous Stop, Next Stop, Go to Start, Go to End.
4. **Representación visual de la ruta**: dibujar en un `Canvas` (o con `Label`s) cada parada como un círculo o caja conectada por líneas, caminando la lista con un puntero `while`. La parada `current` debe verse resaltada (otro color) y mostrar un bus.
5. **Panel de texto** que muestre el recorrido de ida y de vuelta (`forward_text`, `backward_text`).
6. **Barra de estado** con mensajes claros: éxito, "stop not found", "duplicate name", "empty name", "route is empty".
7. Contador visible con el total de paradas (`size`).

La interfaz se redibuja después de cada operación. Como no se usan listas, el redibujado se hace limpiando el `Canvas` y recorriendo desde `head` con un puntero.

## 8. Estilo de código

- Nombres en `snake_case` para métodos y variables, `PascalCase` para clases.
- Cada método lleva un docstring corto en inglés que indique qué hace y su complejidad (por ejemplo, `O(1)` o `O(n)`).
- Comentarios solo donde aclaren el manejo de punteros (por ejemplo, los cuatro enlaces al insertar en medio).
- Métodos cortos y con una sola responsabilidad. Sin código duplicado: la búsqueda se reutiliza en `add_after`, `add_before`, `remove` y `go_to`.
- Sin variables globales mutables.

## 9. Casos borde que siempre se prueban

1. Agregar, buscar, eliminar y navegar en una ruta vacía.
2. Agregar el primer nodo y verificar `head`, `tail` y `current`.
3. Eliminar el único nodo.
4. Eliminar `head`, `tail` y un nodo del medio.
5. Eliminar la parada `current` en cada uno de esos casos.
6. `add_after` sobre `tail` y `add_before` sobre `head`.
7. `move_next` en `tail` y `move_prev` en `head`.
8. Nombres duplicados y nombres vacíos.
9. Verificar el invariante 4 (`n.next.prev is n`) después de cada operación.

## 10. Flujo de trabajo del agente

1. Lee esta guía completa antes de responder.
2. Implementa primero `stop.py` y `bus_route.py`, y pruébalos con un `main.py` de consola mínimo.
3. Cuando la lógica esté correcta, implementa `ui.py` conectándolo solo por los métodos públicos.
4. Antes de entregar, ejecuta la **lista de verificación** de la sección 11.
5. Explica al usuario las decisiones sobre punteros de forma clara; es un taller académico y debe poder sustentarlo.

## 11. Lista de verificación antes de entregar

- [ ] No aparece `[` ni `]` en ningún archivo `.py`.
- [ ] No hay `list`, `tuple`, `dict`, `set` ni `deque` almacenando paradas.
- [ ] No hay `len()`, `range`, `enumerate`, `append`, `pop`, `join` ni `split`.
- [ ] No hay imports en `stop.py` ni `bus_route.py`; `tkinter` solo en `ui.py`.
- [ ] Todo el código, comentarios y textos de la interfaz están en inglés.
- [ ] Los recorridos usan un puntero auxiliar y `while`.
- [ ] Los seis invariantes de la sección 5.2 se cumplen tras cada operación.
- [ ] Los casos borde de la sección 9 funcionan.
- [ ] `ui.py` no modifica `prev` ni `next` directamente.
- [ ] El programa se ejecuta con `python main.py` sin instalar nada.
