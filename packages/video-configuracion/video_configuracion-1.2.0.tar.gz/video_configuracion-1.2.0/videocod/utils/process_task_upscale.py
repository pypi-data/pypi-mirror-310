import requests
import json
import time
from tqdm import tqdm
import re  # Importar módulo de expresiones regulares

def get_task_details(task_id, jwt_token):
    url = f"https://api.vidu.studio/vidu/v1/tasks/{task_id}"

    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "Accept-Language": "en",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Origin": "https://www.vidu.studio/",
        "Referer": "https://www.vidu.studio/",
        "Cache-Control": "no-cache",
        "Cookie": f"sajssdk_2015_cross_new_user=1; _ga=GA1.1.77204265.1725572952; amp_af43d4=61603120ab0445398cd1cb92fd88aef0...1i727srs7.1i727ujms.6.1.7; JWT={jwt_token}; Shunt=; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sSEGIEItsRRRsHGE%22%2C%22gae28_aV%22%3A%22EGEySsGigsIHGA-AsSSHnIgEEySVVs-snAAEEHE-EsGnAAA-EGEySsGigsSisH%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlJPhNcpZTowqwEpF08wX3AQXKswsPJwZwAW9NcBF3swX0JwFKJBF1cpFPMwX08wFlJPhNcpZTowq7zwqKaBv3liZ7ku67OV5kgu9G6iZHgiZNapa3cQX1Hwh1hpX3IQhycQFlJ36A%3D%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sSEGIEItsRRRsHGE%22%7D%7D; _ga_ZJBV7VYP55=GS1.1.1725576214.2.1.1725578996.0.0.0",
        "Accept-Encoding": "gzip, deflate"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching task details: {response.status_code}")
        return 'ID no encontrado', 'URI no encontrado'

    response_json = response.json()
    creations = response_json.get('creations', [])
    if creations and isinstance(creations, list) and len(creations) > 0:
        creation_id = creations[0].get('id', 'ID no encontrado')
        creation_uri = creations[0].get('uri', 'URI no encontrado')
    else:
        creation_id = 'ID no encontrado'
        creation_uri = 'URI no encontrado'

    return creation_id, creation_uri

def descargar_video(uri, nombre_archivo):
    response = requests.get(uri, stream=True)

    if response.status_code == 200:
        with open(nombre_archivo, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"\nVideo descargado y guardado como {nombre_archivo}")
    else:
        print("\nError al descargar el video")

def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.readline().strip()  # Leer el archivo y eliminar espacios
            return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def write_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
    except IOError as e:
        print(f"Error writing file: {e}")

def processupscaler():
    task_id_path = "/tmp/task_id_upscale.txt"
    jwt_token_path = "/tmp/jwt_token.txt"
    creation_id_path = "/tmp/creation_id.txt"

    task_id = read_file(task_id_path)
    jwt_token = read_file(jwt_token_path)
    print(task_id)

    if not task_id or not jwt_token:
        print("No se pudo leer task_id o jwt_token. Asegúrate de que los archivos existan y contengan la información correcta.")
        return

    # Usar expresión regular para extraer solo el número del task_id en caso que esté en un formato especial
    task_id = re.search(r'\d+', task_id).group() if task_id else None

    while True:
        with tqdm(total=10, desc="Esperando 10 segundos", ncols=80, leave=False) as pbar:
            for _ in range(10):
                time.sleep(1)
                pbar.update(1)

        creation_id, creation_uri = get_task_details(task_id, jwt_token)

        if creation_id != 'ID no encontrado' and creation_uri != 'URI no encontrado':
            #print(f"\nCreación encontrada: ID: {creation_id}, URI: {creation_uri}")
            write_file(creation_id_path, creation_id)  # Guardar el creation_id en un archivo
            descargar_video(creation_uri, "/tmp/rt32gaarfcaghattasc/video.mp4")
            break
        else:
            # Imprimir el mensaje de error en la misma línea
            pbar.set_description("No se ha encontrado el ID o URI, intentando de nuevo...")
            pbar.refresh()

#if __name__ == "__main__":
#    main()