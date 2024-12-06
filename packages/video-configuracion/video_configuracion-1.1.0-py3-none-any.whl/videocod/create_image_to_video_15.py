import requests
import uuid
import argparse

def send_img_to_video_task(jwt_token, token_aws, text_content, image_content, enhance, 
                           resolution, movement_amplitude):

    url = "https://api.vidu.studio/vidu/v1/tasks"

    headers = {
        "Host": "api.vidu.studio",
        "Connection": "keep-alive",
        "X-Request-Id": str(uuid.uuid4()),
        "sec-ch-ua-platform": "Windows",
        "Accept-Language": "en",
        "x-recaptcha-token": "Task_Submit",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "X-Aws-Waf-Token": token_aws,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.vidu.studio",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.vidu.studio/",
        "Cookie": f"sajssdk_2015_cross_new_user=1; _ga=GA1.1.77204265.1725572952; amp_af43d4=61603120ab0445398cd1cb92fd88aef0...1i727srs7.1i727ujms.6.1.7; JWT={jwt_token}; Shunt=; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22sSEGIEItsRRRsHGE%22%2C%22gae28_aV%22%3A%22EGEySsGigsIHGA-AsSSHnIgEEySVVs-snAAEEHE-EsGnAAA-EGEySsGigsSisH%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlJPhNcpZTowqwEpF08wX3AQXKswsPJwZwAW9NcBF3swX0JwFKJBF1cpFPMwX08wFlJPhNcpZTowq7zwqKaBv3liZ7ku67OV5kgu9G6iZHgiZNapa3cQX1Hwh1hpX3IQhycQFlJ36A%3D%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%24aVr68a8c_kmfa6_aV%22%2C%22Cikbr%22%3A%22sSEGIEItsRRRsHGE%22%7D%7D; _ga_ZJBV7VYP55=GS1.1.1725576214.2.1.1725578996.0.0.0",
        "Accept-Encoding": "gzip, deflate",
    }

    payload = {
        "input": {
            "prompts": [
                {"type": "text", "content": text_content},
                {"type": "image", "content": f"ssupload:?id={image_content}", "src_img": f"ssupload:?id={image_content}"}
            ],
            "enhance": enhance
        },
        "type": "img2video",
        "settings": {
            "duration": 4,
            "resolution": resolution,
            "movement_amplitude": movement_amplitude,
            "model_version": "1.5"
        }
    }

    try:
        # Realizar la solicitud POST
        response = requests.post(url, headers=headers, json=payload)
        
        # Verificar el código de estado HTTP
        if response.status_code == 200:
            response_json = response.json()
            print("Solicitud aceptada, procesamiento en curso...")
            #print(f"Respuesta: {response_json}")
            return response_json.get('id', 'ID no encontrado')
        else:
            print(f"Error: Código de estado {response.status_code}")
            #print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
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

def read_file_info(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) >= 1:
                file_id = lines[0].strip().split(': ')[1]
                return file_id
            else:
                print("File does not contain enough lines.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError as e:
        print(f"Error reading file: {e}")

def read_jwt_token(file_path):
    try:
        with open(file_path, "r") as file:
            token = file.readline().strip()
            return token
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError as e:
        print(f"Error reading file: {e}")

def save_task_id(file_path, task_id):
    try:
        with open(file_path, "w") as file:
            file.write(f"task_id: {task_id}")
    except IOError as e:
        print(f"Error writing file: {e}")

def gen_image_to_video_15(text_content, enhance, resolution, movement_amplitude):
    #parser = argparse.ArgumentParser(description="Crea una tarea de video basada en texto e imagen usando la API de Vidu Studio.")
    #parser.add_argument('--text', type=str, required=True, help="Texto para generar el video.")
    #parser.add_argument('--resolution', type=str, default="512", help="Resolución del video (e.g., 512).")
    #parser.add_argument('--movement_amplitude', type=str, default="auto", help="Amplitud de movimiento (e.g., auto).")
    #parser.add_argument('--enhance', type=bool, default=True, help="Habilitar mejora de calidad (True o False).")

    #args = parser.parse_args()

    file_info_path = "/tmp/file_info.txt"  # Ruta al archivo que contiene file_id
    jwt_token_path = "/tmp/jwt_token.txt"   # Ruta al archivo que contiene el jwt_token
    task_id_path = "/tmp/task_id.txt"       # Ruta al archivo donde se guardará el task_id

    file_id = read_file_info(file_info_path)
    jwt_token = read_jwt_token(jwt_token_path)
    token_swt =  leer_token()

    if file_id and jwt_token:
        try:
            
            #task_id = create_task(args.prompt, token_swt, file_id, jwt_token, enhance=args.enhance, model=args.model)
            task_id = send_img_to_video_task(
            jwt_token,
            token_swt,
            text_content,
            file_id,
            enhance,
            resolution,
            movement_amplitude
    )
            #print(f"El ID de la tarea es: {task_id}")
            save_task_id(task_id_path, task_id)
        except Exception as e:
            print(e)

#if __name__ == "__main__":
#    main()
