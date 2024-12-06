import argparse
import requests
import uuid
import subprocess
from file_uploader_with_etag import *


def upload_file_to_vidu(jwt_token, token_aws):

    url = "https://api.vidu.studio/tools/v1/files/uploads"

    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "Accept-Language": "en",
        "sec-ch-ua-mobile": "?0",
        "X-Aws-Waf-Token": f"{token_aws}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "X-Request-Id": str(uuid.uuid4()),
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Origin": "https://www.vidu.studio",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.vidu.studio/",
        "Cookie": f"sajssdk_2015_cross_new_user=1; _ga=GA1.1.77204265.1725572952; amp_af43d4=61603120ab0445398cd1cb92fd88aef0...1i727srs7.1i727ujms.6.1.7; JWT={jwt_token}; Shunt=; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sSEGIEItsRRRsHGE%22%2C%22gae28_aV%22%3A%22EGEySsGigsIHGA-AsSSHnIgEEySVVs-snAAEEHE-EsGnAAA-EGEySsGigsSisH%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlJPhNcpZTowqwEpF08wX3AQXKswsPJwZwAW9NcBF3swX0JwFKJBF1cpFPMwX08wFlJPhNcpZTowq7zwqKaBv3liZ7ku67OV5kgu9G6iZHgiZNapa3cQX1Hwh1hpX3IQhycQFlJ36A%3D%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sSEGIEItsRRRsHGE%22%7D%7D; _ga_ZJBV7VYP55=GS1.1.1725576214.2.1.1725578996.0.0.0",
    }

    payload = {
        "scene": "vidu"
    }

    try:
        # Enviar la solicitud POST
        response = requests.post(url, headers=headers, json=payload)

        # Procesar la respuesta
        response_json = response.json()
        file_id = response_json.get("id")
        put_url = response_json.get("put_url")

        # Mostrar los valores extraídos
        print(f"ID: {file_id}")
        #print(f"PUT URL: {put_url}")

        return file_id, put_url

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"Error decoding JSON: {e}")

def save_to_txt(file_id, put_url, filename):
    with open(filename, "w") as file:
        file.write(f"file_id: {file_id}\n")
        file.write(f"put_url: {put_url}\n")
    #print(f"Data saved to {filename}")

def read_jwt_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            jwt_token = file.read().strip()
        return jwt_token
    except FileNotFoundError:
        print(f"File not found: jwtToken")
    except IOError as e:
        print(f"Error reading file: {e}")

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

def fileuploader(file_info_name, image_name):
    # Configurar argparse dentro de la función main
    #parser = argparse.ArgumentParser(description="Subir archivos a Vidu Studio")
    #parser.add_argument("--file_info", type=str, required=True, help="Nombre del archivo de información a guardar")
    #parser.add_argument("--image", type=str, required=True, help="Nombre base del archivo de imagen (sin extensión)")
    
    # Parsear los argumentos
    #args = parser.parse_args()
    #file_info_name = args.file_info
    #image_name = args.image
    
    jwt_file_path = "/tmp/jwt_token.txt"  # Ruta al archivo que contiene el JWT
    jwt_token = read_jwt_from_file(jwt_file_path)
    token_swt = leer_token()
    
    if jwt_token:
        file_id, put_url = upload_file_to_vidu(jwt_token, token_swt)
        if file_id and put_url:
            save_to_txt(file_id, put_url, filename=f"/tmp/{file_info_name}.txt")
    
    file_up_etag(file_info_name, image_name)

#if __name__ == "__main__":
#    main()
