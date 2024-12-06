import urllib.request
import json
import subprocess
import argparse

# Función para cargar el JWT token desde un archivo
def cargar_jwt_token(ruta='/tmp/jwt_token.txt'):
    try:
        with open(ruta, 'r') as archivo:
            jwt_token = archivo.read().strip()
            return jwt_token
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado.")
        subprocess.run(["python", "/tmp/rt32gaarfcaghattasc/main.py"], check=True)
        return None

# Función para obtener los créditos utilizando el JWT token
def obtener_credits(jwt_token, credit_comparar):
    url = "https://api.vidu.studio/vidu/v1/tasks/credits?type=img2video&settings.duration=4&settings.model=vidu-1"
    headers = {
        "Host": "api.vidu.studio",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "Accept-Language": "en",
        "sec-ch-ua-mobile": "?0",
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

    request = urllib.request.Request(url, headers=headers, method='GET')

    try:
        # Realizar la solicitud y obtener la respuesta
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            #print("Response:", response_body)
            data = json.loads(response_body)
            
            # Extraer 'current_credits' de la respuesta
            current_credits = data.get('current_credits')
            if current_credits is not None:
                print(f"Current Credits: {current_credits}")
                # Comparar los créditos y ejecutar el comando si es igual al valor proporcionado
                if current_credits == credit_comparar or current_credits == 0:
                    print(f"Créditos iguales a {credit_comparar}. Ejecutando /content/main.py...")
                    subprocess.run(["python", "/tmp/rt32gaarfcaghattasc/main.py"], check=True)
                else:
                    print(f"Los créditos no son {credit_comparar}.")
            else:
                print("No se encontró 'current_credits' en la respuesta.")
    except urllib.error.HTTPError as e:
        print(f"Error HTTP: {e.code}")
        print(f"Detalles del error: {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"Error de conexión: {e.reason}")

# Ejecutar el script principal
def credits(credit):
    jwt_token = cargar_jwt_token()
    if jwt_token:
        obtener_credits(jwt_token, credit)

"""if __name__ == "__main__":
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Verificar créditos y ejecutar un script basado en el valor de créditos.')
    parser.add_argument('--credit', type=int, default=4, help='El valor de créditos para comparar (predeterminado es 4).')
    args = parser.parse_args()

    jwt_token = cargar_jwt_token()
    if jwt_token:
        obtener_credits(jwt_token, args.credit)"""
