# SimpleLogs

**SimpleLogs** es una biblioteca de código abierto ligera y fácil de usar para crear registros (logs) con colores personalizables en Python. Ideal para desarrolladores que buscan simplificar el seguimiento y la depuración en sus proyectos.
- Colores en los mensajes de log.
- Diferentes niveles de log (`INFO`, `WARNING`, `ERROR`, `TRACE`).
- Opcional: Mostrar la línea del código donde se generó el mensaje.

## Instalación
Primero, clona este repositorio y añade SimpleLogs a tu proyecto:

```bash
git clone https://github.com/Pabl0VC/simpleLogs.git
# /simpleLogs/ Agrega esta carpeta a tu proyecto. Idealmente en /modules/
```
Si usas un entorno virtual, asegúrate de activarlo e instala los requerimientos:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Uso Básico
Importa SimpleLogs en tu proyecto:
```python
from simpleLogs import info, warning, error, trace

info("Mensaje de información")
warning("Mensaje de advertencia")
error("Mensaje de error")
trace("Mensaje de depuración")
```

Si deseas incluir información sobre la línea donde se genera el mensaje, utiliza las funciones con sufijo **L**:
```python
from simpleLogs import infoL, warningL, errorL, traceL

infoL("Información con línea de código")
```

## Características
- Colores personalizables: Cada nivel de log tiene un color único para facilitar la identificación visual.
- Formato enriquecido: Muestra la fecha, hora y línea de origen opcionalmente.
- Ligero y fácil de integrar: Ideal para proyectos grandes o pequeños.
- Soporte para niveles avanzados: Incluye trazabilidad (trace) para depuración detallada.
- Fácil integración: Diseñado para usarse como un reemplazo rápido y sencillo de `print()`.


## Niveles de Log Soportados
SimpleLogs soporta los siguientes niveles de log, cada uno con colores personalizados para una mejor visibilidad:

| Nivel      | Descripción                              | Variantes               |
|------------|------------------------------------------|-------------------------|
| **INFO**   | Mensajes informativos.                  | `info`, `infoL`         |
| **WARNING**| Advertencias sobre posibles problemas.   | `warning`, `warningL`   |
| **ERROR**  | Mensajes de error críticos.             | `error`, `errorL`       |
| **TRACE**  | Mensajes para depuración detallada.      | `trace`, `traceL`       |

### Imágenes
![alt text](/examples/example_terminal.png)

### Real Examples
![alt text](/examples/real_ex.png)

## Requisitos
- Python 3.7 o superior
- colorama

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto
Creado por Pablo Vega Castro. Si tienes dudas o sugerencias, no dudes en contactarme pablovegac.93@gmail.com.