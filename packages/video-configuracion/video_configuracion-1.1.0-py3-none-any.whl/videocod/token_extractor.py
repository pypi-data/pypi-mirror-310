import undetected_chromedriver as uc
from selenium import webdriver
import time
import json
import re
import threading
import random  # Importar el módulo random para la selección aleatoria de User-Agent

# Bandera de parada global
detener_hilo = False

# Lista extensa de User-Agents posibles
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
]

# Seleccionar un User-Agent aleatorio
user_agent = random.choice(user_agents)

# Configuración de las opciones de Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')  # Modo sin cabeza
chrome_options.add_argument('--enable-javascript')
chrome_options.add_argument('--disable-gpu')
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # Logs de rendimiento

# Establecer el User-Agent aleatorio
chrome_options.add_argument(f'user-agent={user_agent}')

# Lanzar el navegador con undetected_chromedriver
driver = uc.Chrome(options=chrome_options)
driver.implicitly_wait(6.5)

# Habilitar el protocolo DevTools para acceder a los eventos de red
driver.execute_cdp_cmd("Network.enable", {})

# Función para extraer el token de los datos de la solicitud
def extraer_token(texto):
    inicio = r'"existing_token":"'
    final = r'",\"awswaf_session_storage\"'

    coincidencia = re.search(f"{inicio}(.*?){final}", texto)

    if coincidencia:
        return coincidencia.group(1)
    return None

# Función para leer los logs de red y buscar el existing_token
def print_network_logs(driver, debug=False):
    logs = driver.get_log("performance")
    token = None  # Inicializa token a None
    for log in logs:
        message = log["message"]
        try:
            log_dict = json.loads(message)  # Intentar cargar el mensaje como JSON
            postData = log_dict['message']['params']['request'].get('postData')
            if postData and 'existing_token' in postData:
                token = extraer_token(postData)
                if token and token != "null":  # Verifica si el token no es null
                    print(f"Token extraído: {token}")
                    return token  # Detener la búsqueda una vez encontrado un token válido
        except json.JSONDecodeError as e:  # Si el JSON está malformado
            if debug:
                print(f"Error al procesar el JSON: {e}")
                print(f"Mensaje problemático: {message}")
        except KeyError as e:  # Si alguna clave falta en el diccionario
            if debug:
                print(f"Error de clave faltante: {e}")
        except Exception as e:  # Captura cualquier otro error inesperado
            if debug:
                print(f"Error inesperado: {e}")
    return token  # Retorna None o el token si se encontró

# Función para guardar el token en un archivo de texto (se sobrescribe siempre)
def guardar_token_en_archivo(token):
    try:
        # Escribir el token en el archivo /tmp/token_swt.txt (sobrescribe siempre)
        with open("/tmp/token_swt.txt", "w") as file:
            file.write(token)
    except Exception as e:
        print(f"Error al guardar el token en el archivo: {e}")

# Función que se ejecuta en bucle cada 40 segundos
def obtener_token_periodicamente():
    global detener_hilo  # Acceder a la bandera global
    
    driver.get("https://www.vidu.studio/login")

    while not detener_hilo:
        try:
            driver.refresh()  # Refrescar la página
            time.sleep(10)
            # Intentar capturar el token
            token = print_network_logs(driver, debug=False)
            
            if token:  # Si se encuentra un token válido
                guardar_token_en_archivo(token)
            else:
                print("No se encontró el token en esta iteración.")
        except Exception as e:  # Captura cualquier error del bucle
            print(f"Error en el bucle principal: {e}")
        
        # Esperar 40 segundos antes de repetir el proceso
        time.sleep(40)

# Función para iniciar el hilo
def iniciar_hilo():
    global detener_hilo
    # Crear un hilo que ejecute la función obtener_token_periodicamente
    hilo = threading.Thread(target=obtener_token_periodicamente, daemon=True)
    hilo.start()

# Función para detener el hilo
def detener_ejecucion():
    global detener_hilo
    detener_hilo = True  # Cambiar la bandera para que el hilo termine

# Iniciar el hilo
if __name__ == "__main__":
    iniciar_hilo()

    # Mantener el hilo principal activo para que no termine inmediatamente
    while True:
        time.sleep(1)  # Puedes hacer otras tareas aquí si lo deseas
        # Para detener el script, puedes llamar a la función detener_ejecucion()
