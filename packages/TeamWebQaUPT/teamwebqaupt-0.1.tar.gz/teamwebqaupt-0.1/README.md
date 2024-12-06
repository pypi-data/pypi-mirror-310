
# TeamWebQaUPT

**TeamWebQaUPT** es un paquete diseñado para realizar pruebas automatizadas de interfaces web utilizando Selenium y pytest. Proporciona herramientas reutilizables y fáciles de usar para simplificar el proceso de pruebas.

## **Características Principales**
- Configuración automática de navegadores utilizando Selenium.
- Ejecución de pruebas paralelas con pytest-xdist.
- Reportes de resultados en formato Allure.
- Funciones reutilizables para interacciones comunes como dropdowns, validaciones y navegación.

---

## **Instalación**

### Requisitos Previos
1. Tener instalado **Python 3.7** o superior.
2. Instalar pip (administrador de paquetes de Python).
3. Tener Selenium Grid configurado y en ejecución (opcional para pruebas locales, pero necesario para pruebas distribuidas).

### Instalación del Paquete
1. Instala el paquete desde PyPI:
   ```bash
   pip install TeamWebQaUPT
   ```

2. Verifica la instalación:
   ```bash
   python -c "import TeamWebQaUPT; print('Instalación exitosa')"
   ```

---

## **Ejecución de Pruebas**

### Comando para Ejecutar Todas las Pruebas
El paquete incluye un script que ejecuta todas las pruebas automáticamente y genera un reporte Allure:
```bash
ejecutar_pruebas
```

Por defecto, el comando:
- Ejecuta pruebas en paralelo utilizando 3 procesos (`-n 3`).
- Genera resultados en el directorio `allure-results`.

### Ver Resultados con Allure
Para visualizar los resultados en formato Allure:
1. Instala Allure:
   ```bash
   brew install allure  # En macOS
   sudo apt install allure  # En Linux
   ```
   [Instrucciones de instalación para Windows](https://docs.qameta.io/allure/#_get_started).

2. Sirve los resultados generados:
   ```bash
   allure serve allure-results
   ```

---

## **Funciones Reutilizables**

El paquete incluye una serie de funciones reutilizables en el módulo `utils.py`. Aquí hay una lista de las más útiles:

### 1. **Seleccionar Opción en Dropdown**
```python
from TeamWebQaUPT.utils import select_dropdown_option

select_dropdown_option(driver, dropdown_id="facultad", option_text="Facultad de Ingeniería")
```

**Descripción**:
- Selecciona una opción en un combo box (dropdown) por texto visible.

**Parámetros**:
- `driver`: Instancia de Selenium WebDriver.
- `dropdown_id`: ID del dropdown en el DOM.
- `option_text`: Texto visible de la opción a seleccionar.

---

### 2. **Validar Elementos en una Lista**
```python
from TeamWebQaUPT.utils import validate_elements_in_list

validate_elements_in_list(driver, "//h3[contains(text(), '{}')]", ["Equipo A", "Equipo B"])
```

**Descripción**:
- Verifica que una lista de elementos esté visible en la página.

**Parámetros**:
- `driver`: Instancia de Selenium WebDriver.
- `xpath_template`: Plantilla de XPath para encontrar los elementos (usa `{}` para insertar el texto del elemento).
- `items`: Lista de textos a validar.

---

### 3. **Navegar por Menús**
```python
from TeamWebQaUPT.utils import navigate_menu

navigate_menu(
    driver,
    menu_items={
        "Inicio": "http://161.132.50.153/",
        "Eventos": "http://161.132.50.153/eventos"
    },
    base_url="http://161.132.50.153/equipos"
)
```

**Descripción**:
- Navega por un menú y valida la navegación de URLs.

**Parámetros**:
- `driver`: Instancia de Selenium WebDriver.
- `menu_items`: Diccionario con texto del menú como clave y URL esperada como valor.
- `base_url`: URL base para regresar después de cada navegación.

---

### 4. **Procesar Tablas Gherkin**
```python
from TeamWebQaUPT.utils import process_table_data

table_data = [
    ["Equipo"],
    ["Equipo A"],
    ["Equipo B"]
]
processed_data = process_table_data(table_data)
```

**Descripción**:
- Convierte datos de una tabla en un formato reutilizable.

**Parámetros**:
- `table_data`: Lista de listas con los datos de la tabla (primera fila como encabezados).

**Retorno**:
- Una lista de diccionarios con claves basadas en la primera fila.

---

## **Ejemplo Completo de Uso**

```python
from TeamWebQaUPT.utils import (
    select_dropdown_option,
    validate_elements_in_list,
    navigate_menu
)
from selenium import webdriver

# Configuración inicial
driver = webdriver.Chrome()

try:
    # Abrir página inicial
    driver.get("http://161.132.50.153/")

    # Seleccionar una opción en un dropdown
    select_dropdown_option(driver, "facultad", "Facultad de Ingeniería")

    # Validar elementos en una lista
    validate_elements_in_list(driver, "//h3[contains(text(), '{}')]", ["Equipo A", "Equipo B"])

    # Navegar por el menú
    navigate_menu(
        driver,
        {"Inicio": "http://161.132.50.153/", "Eventos": "http://161.132.50.153/eventos"},
        "http://161.132.50.153/"
    )
finally:
    driver.quit()
```

---

## **Contribuciones**

Si deseas contribuir al desarrollo de **TeamWebQaUPT**, sigue estos pasos:
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/TeamWebQaUPT
   cd TeamWebQaUPT
   ```

2. Instala las dependencias para desarrollo:
   ```bash
   pip install -r requirements.txt
   ```

3. Crea tus cambios y envía un pull request.

---

## **Licencia**
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

