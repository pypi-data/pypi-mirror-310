import requests
import argparse
import uuid

def create_video_task(jwt_token, token_aws, prompt, aspect_ratio, enhance, model, style):

    url = "https://api.vidu.studio/vidu/v1/tasks"
    
    headers = {
        "Host": "api.vidu.studio",
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
        "Accept-Encoding": "gzip, deflate"
    }
    
    payload = {
        "input": {
            "prompts": [
                {
                    "type": "text",
                    "content": prompt,
                    "enhance": enhance
                }
            ]
        },
        "type": "text2video",
        "settings": {
            "style": style,
            "aspect_ratio": aspect_ratio,  # Relación de aspecto editable
            "duration": 4,
            "model": model #"vidu-1"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()
    task_id = response_json.get('id', 'ID no encontrado')

    return task_id

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

def save_task_id(file_path, task_id):
    try:
        with open(file_path, "w") as file:
            file.write(f"task_id: {task_id}")
    except IOError as e:
        print(f"Error writing file: {e}")

def gen_text_to_video(prompt, aspect_ratio, enhance, model, style):
    # Configurar el análisis de argumentos
    #parser = argparse.ArgumentParser(description="Create a video task using the Vidu API.")
    #parser.add_argument('--prompt', type=str, required=True, help="The text prompt to generate the video.")
    #parser.add_argument('--aspect_ratio', type=str, default="16:9", help="The aspect ratio of the video (e.g., 16:9, 1:1, 4:3).")
    #parser.add_argument('--enhance', type=bool, default=True, help='Habilitar mejora (True o False)')
    #parser.add_argument('--model', type=str, required=True, help='vidu-1')
    #parser.add_argument('--style', type=str, required=True, help='general')

    #args = parser.parse_args()

    # Leer el JWT token desde el archivo
    with open('/tmp/jwt_token.txt', 'r') as file:
        jwt_token = file.read().strip()
    
    token_swt = leer_token()
    # Llamar a la función con el argumento del prompt y el aspect_ratio
    task_id = create_video_task(jwt_token, token_swt, prompt, aspect_ratio, enhance, model, style)
    #print(f"El ID de la tarea es: {task_id}")

    # Guardar el task_id en un archivo
    save_task_id('/tmp/task_id.txt', task_id)

#if __name__ == "__main__":
#    main()

