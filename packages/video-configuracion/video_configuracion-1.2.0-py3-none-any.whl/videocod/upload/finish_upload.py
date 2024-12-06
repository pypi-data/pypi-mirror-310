import argparse
import requests

def finish_upload(upload_id, etag, jwt_token):
    url = f"https://api.vidu.studio/tools/v1/files/uploads/{upload_id}/finish"
    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-platform": '"Windows"',
        "Accept-Language": "en",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.vidu.studio",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.vidu.studio/",
        "Cookie": f"JWT={jwt_token}",
        "Accept-Encoding": "gzip, deflate"
    }
    payload = {
        "id": upload_id,
        "etag": etag
    }

    response = requests.put(url, headers=headers, json=payload)
    print(f"ETag: {etag}")

    # Verificando el estado de la respuesta
    return response.text

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
        print(f"File not found: file_info or etag_info")
    except IOError as e:
        print(f"Error reading file: {e}")

def read_etag(file_path):
    try:
        with open(file_path, "r") as file:
            line = file.readline().strip()
            etag = line.split(': ')[1] if ': ' in line else None
            return etag
    except FileNotFoundError:
        print(f"File not found: etag_info")
    except IOError as e:
        print(f"Error reading file: {e}")

def read_jwt_token(file_path):
    try:
        with open(file_path, "r") as file:
            token = file.readline().strip()
            return token
    except FileNotFoundError:
        print(f"File not found: jwtToken")
    except IOError as e:
        print(f"Error reading file: {e}")


def finish(file_info):
    # Usamos argparse para permitir la personalización del nombre del archivo de información
    #parser = argparse.ArgumentParser(description="Finalizar la subida de archivos a Vidu Studio")
    #parser.add_argument("--file_info", type=str, required=True, help="Nombre base del archivo de información (sin extensión)")

    #args = parser.parse_args()

    # Crear las rutas de archivo usando los nombres proporcionados
    file_info_path = f"/tmp/{file_info}.txt"  # Ruta al archivo de información (editable)
    etag_info_path = "/tmp/etag_info.txt"   # Ruta al archivo que contiene el etag
    jwt_token_path = "/tmp/jwt_token.txt"   # Ruta al archivo que contiene el jwt_token

    file_id, put_url = read_file_info(file_info_path)
    etag = read_etag(etag_info_path)
    jwt_token = read_jwt_token(jwt_token_path)

    if file_id and etag and jwt_token:
        try:
            result = finish_upload(file_id, etag, jwt_token)
            #print(result)  # Puedes descomentar si quieres ver la respuesta
        except Exception as e:
            print(e)

#if __name__ == "__main__":
#    main()