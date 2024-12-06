import argparse
import requests
import subprocess
from videocod.upload.finish_upload import *


def upload_file_to_vidu(upload_url, file_path):
    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "Content-Type": "image/*",  # Asegúrate de que el tipo de contenido coincida con el archivo que estás subiendo
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Origin": "https://www.vidu.studio",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.vidu.studio/",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    with open(file_path, 'rb') as file:
        response = requests.put(upload_url, headers=headers, data=file)

    # Verificando el estado de la respuesta
    if response.status_code == 200:
        # Capturando los encabezados de la respuesta
        response_headers = response.headers
        # Extrayendo el valor del encabezado ETag
        etag = response_headers.get('ETag', 'Encabezado ETag no encontrado')
        return etag.replace('"', '')
    else:
        raise Exception(f"Error al subir el archivo: {response.status_code}")

def save_etag_to_txt(etag, filename="/tmp/etag_info.txt"):
    with open(filename, "w") as file:
        file.write(f"ETag: {etag}\n")
    print(f"ETag saved to {etag}")

def read_file_info(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                file_id = lines[0].strip().split(': ')[1]
                put_url = lines[1].strip().split(': ')[1]
                return file_id, put_url
            else:
                print("File does not contain enough lines.")
    except FileNotFoundError:
        print(f"File not found: file_info or Image")
    except IOError as e:
        print(f"Error reading file: {e}")

def file_up_etag(file_info, image_path):
    print("uplaodr 2")
    # Usamos argparse para obtener los nombres de los archivos
    #parser = argparse.ArgumentParser(description="Subir un archivo a Vidu Studio y obtener el ETag")
    #parser.add_argument("--file_info", type=str, required=True, help="Nombre base del archivo de información (sin extensión)")
    #parser.add_argument("--image", type=str, required=True, help="Nombre base del archivo de imagen (sin extensión)")

    # Parsear los argumentos de la línea de comandos
    #args = parser.parse_args()

    # Construir las rutas de archivo usando los nombres proporcionados
    file_info_path = f"/tmp/{args.file_info}.txt"  # Ruta al archivo de información
    image_path = f"/tmp/{args.image}.jpg"          # Ruta al archivo de imagen

    # Leer file_info.txt
    file_id, put_url = read_file_info(file_info_path)
    
    if put_url:
        try:
            # Subir el archivo y obtener el ETag
            etag = upload_file_to_vidu(put_url, image_path)
            # Guardar el ETag en un archivo
            save_etag_to_txt(etag)
        except Exception as e:
            print(e)


    finish(file_info)

#if __name__ == "__main__":
#    main()