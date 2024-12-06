import requests
import re

def read_task_id(file_path):
    """
    Leer el task_id desde un archivo, eliminando el texto extra y dejando solo el número.
    """
    try:
        with open(file_path, "r") as file:
            task_id_line = file.readline().strip()
            # Usar una expresión regular para extraer solo el número del task_id
            match = re.search(r'\d+', task_id_line)
            if match:
                return match.group(0)
            else:
                print("No se encontró un task_id válido.")
                return None
    except FileNotFoundError:
        print(f"Archivo no encontrado: {file_path}")
        return None
    except IOError as e:
        print(f"Error leyendo el archivo: {e}")
        return None

def read_jwt_token(file_path):
    """
    Leer el jwt_token desde un archivo.
    """
    try:
        with open(file_path, "r") as file:
            return file.readline().strip()
    except FileNotFoundError:
        print(f"Archivo no encontrado: {file_path}")
        return None
    except IOError as e:
        print(f"Error leyendo el archivo: {e}")
        return None

def leer_token():
    try:
        with open("/tmp/token_swt.txt", "r") as file:
            token = file.read()  # Leer el contenido del archivo
            if token:
                return token  # Devuelve el token si se encontró
            else:
                return "El archivo está vacío o no contiene un token."
    except Exception as e:
        return f"Error al leer el archivo: {e}"

def delete_task(task_id, jwt_token, token_aws):

    """
    Eliminar la tarea usando el task_id y el jwt_token.
    """
    url = f"https://api.vidu.studio/vidu/v1/tasks/{task_id}"

    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "Accept-Language": "en",
        "sec-ch-ua-mobile": "?0",
        "X-Aws-Waf-Token": f"{token_aws}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Origin": "https://www.vidu.studio",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.vidu.studio/",
        "Cookie": f"sajssdk_2015_cross_new_user=1; _ga=GA1.1.77204265.1725572952; amp_af43d4=61603120ab0445398cd1cb92fd88aef0...1i727srs7.1i727ujms.6.1.7; JWT={jwt_token}; Shunt=; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sSEGIEItsRRRsHGE%22%2C%22gae28_aV%22%3A%22EGEySsGigsIHGA-AsSSHnIgEEySVVs-snAAEEHE-EsGnAAA-EGEySsGigsSisH%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlJPhNcpZTowqwEpF08wX3AQXKswsPJwZwAW9NcBF3swX0JwFKJBF1cpFPMwX08wFlJPhNcpZTowq7zwqKaBv3liZ7ku67OV5kgu9G6iZHgiZNapa3cQX1Hwh1hpX3IQhycQFlJ36A%3D%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sSEGIEItsRRRsHGE%22%7D%7D; _ga_ZJBV7VYP55=GS1.1.1725576214.2.1.1725578996.0.0.0",
        "Accept-Encoding": "gzip, deflate"
    }

    # Realizar la solicitud DELETE
    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print(f"Tarea {task_id} eliminada exitosamente.")
    else:
        print(f"Error al eliminar la tarea {task_id}. Código de estado: {response.status_code}")

def deletetaskupscaler():
    task_id_path = "/tmp/task_id_upscale.txt"
    jwt_token_path = "/tmp/jwt_token.txt"

    # Leer task_id y jwt_token desde los archivos correspondientes
    task_id = read_task_id(task_id_path)
    jwt_token = read_jwt_token(jwt_token_path)
    token_swt = leer_token()

    if task_id and jwt_token:
        delete_task(task_id, jwt_token, token_swt)
    else:
        print("Error: No se pudo leer el task_id o el jwt_token.")