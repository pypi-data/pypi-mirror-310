import requests
import uuid


def extract_jwt_cookie(cookies):
    """Extrae el valor de la cookie JWT."""
    jwt_token = cookies.get('JWT')
    return jwt_token

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

def login_to_vidu(correo, codes, token_aws):

    """Inicia sesión en Vidu y devuelve la respuesta y el token JWT."""
    url = "https://api.vidu.studio/iam/v1/users/login"

    headers = {
        "Host": "api.vidu.studio",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "Accept-Language": "en",
        "sec-ch-ua-mobile": "?0",
        "X-Aws-Waf-Token": f"{token_aws}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "X-Request-Id": str(uuid.uuid4()),  # Genera un UUID aleatorio
        "sec-ch-ua-platform": "Windows",
        "Accept": "*/*",
        "Origin": "https://www.vidu.studio",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.vidu.studio/",
        "Cookie": "sajssdk_2015_cross_new_user=1; _ga=GA1.1.77204265.1725572952; amp_af43d4=61603120ab0445398cd1cb92fd88aef0...1i727srs7.1i727ujms.6.1.7; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22EGEySsGigsIHGA-AsSSHnIgEEySVVs-snAAEEHE-EsGnAAA-EGEySsGigsSisH%22%2C%22gae28_aV%22%3A%22%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlJPhNcpZTowqwEpF08wX3AQXKswsPJwZwAW9NcBF3swX0JwFKJBF1cpFPMwX08wFlJPhNcpZTowq7zwqKagN%3D%3D%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%22%2C%22Cikbr%22%3A%22%22%7D%7D; _ga_ZJBV7VYP55=GS1.1.1725576214.2.1.1725578971.0.0.0",
        "Accept-Encoding": "gzip, deflate"
    }

    payload = {
        "id_type": "email",
        "identity": correo,
        "auth_type": "authcode",
        "credential": codes
    }

    response = requests.post(url, headers=headers, json=payload)
    jwt_token = extract_jwt_cookie(response.cookies)
    return response.json(), jwt_token

def send_auth_code(correo, token_aws):

    """Envía un código de autenticación al correo especificado."""
    url = "https://api.vidu.studio/iam/v1/users/send-auth-code"
    headers = {
        "Host": "api.vidu.studio",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "Accept-Language": "en",
        "sec-ch-ua-mobile": "?0",
        "X-Aws-Waf-Token": f"{token_aws}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "X-Request-Id": str(uuid.uuid4()),  # Genera un UUID aleatorio
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Origin": "https://www.vidu.studio",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.vidu.studio/",
        "Cookie": f"sajssdk_2015_cross_new_user=1; _ga=GA1.1.77204265.1725572952; amp_af43d4=61603120ab0445398cd1cb92fd88aef0...1i727srs7.1i727ujms.6.1.7; sensorsdata2015jssdkcross=dfm-enc-%7B%22Va28a6y8_aV%22%3A%22EGEySsGigsIHGA-AsSSHnIgEEySVVs-snAAEEHE-EsGnAAA-EGEySsGigsSisH%22%2C%22gae28_aV%22%3A%22%22%2C%22OemO2%22%3A%7B%22%24ki8r28_8eiggay_2mbeyr_8cOr%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24ki8r28_2rieyz_lrcMmeV%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24ki8r28_ergreere%22%3A%22%22%7D%2C%22aVr68a8ar2%22%3A%22rc3liZ7ku67OV5kgPsGCiskkDskl3qmawFlJPhNcpZTowqwEpF08wX3AQXKswsPJwZwAW9NcBF3swX0JwFKJBF1cpFPMwX08wFlJPhNcpZTowq7zwqKagN%3D%3D%22%2C%22za28mec_kmfa6_aV%22%3A%7B%226ior%22%3A%22%22%2C%22Cikbr%22%3A%22%22%7D%7D; _ga_ZJBV7VYP55=GS1.1.1725576214.2.1.1725578971.0.0.0",
        "Accept-Encoding": "gzip, deflate"
    }
    payload = {
        "channel": "email",
        "receiver": f"{correo}",
        "purpose": "login",
        "locale": "en"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Request successful")
        
    else:
        print(f"Request failed with status code {response.status_code}")
