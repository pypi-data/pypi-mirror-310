from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def select_dropdown_option(driver, dropdown_id, option_text):
    """Selecciona una opción de un dropdown (combo box) por texto visible."""
    try:
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, dropdown_id))
        )
        dropdown.click()
        option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//option[text()='{option_text}']"))
        )
        option.click()
    except Exception:
        driver.execute_script(f"document.getElementById('{dropdown_id}').value = '{option_text}'")

def validate_elements_in_list(driver, xpath_template, items):
    """Valida que una lista de elementos esté visible en la página."""
    for item in items:
        element_xpath = xpath_template.format(item)
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, element_xpath))
        )
        assert element.is_displayed(), f"El elemento '{item}' no está visible."

def navigate_menu(driver, menu_items, base_url):
    """Navega por un menú y valida la navegación de las URLs."""
    for menu, expected_url in menu_items.items():
        menu_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, menu))
        )
        menu_button.click()
        WebDriverWait(driver, 5).until(EC.url_to_be(expected_url))
        driver.get(base_url)

def process_table_data(table_data):
    """Convierte datos de una tabla Gherkin en una lista de diccionarios."""
    headers = table_data[0]
    return [dict(zip(headers, row)) for row in table_data[1:]]
