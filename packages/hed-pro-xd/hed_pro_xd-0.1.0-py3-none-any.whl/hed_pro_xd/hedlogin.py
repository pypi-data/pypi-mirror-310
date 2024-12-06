import requests
import urllib3
from urllib.parse import urlencode
import re
import time
import json

def get_session_info2(formatted_cookies):
    url = "https://www.hedra.com/api/auth/session"
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"{formatted_cookies}",
        "Accept-Encoding": "gzip, deflate"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        print("Response received:")
        #print(response.text)

        # Extraer y formatear las cookies
        cookies = response.cookies
        print("Extraer y formatear las cookies...")
        print(cookies)

        # Buscar la cookie `__Host-next-auth.csrf-token`
        csrf_token = None
        for cookie in cookies:
            if cookie.name == "__Secure-next-auth.session-token":
                csrf_token = cookie.value
                break

        if csrf_token:
            print(f"__Secure-next-auth.session-token: correct...")
        else:
            print("__Secure-next-auth.session-token not found")

        return csrf_token

    except requests.exceptions.RequestException as e:
        print(f"Failed to get session info. Error: {e}")
        return None





def get_session(api_url, formatted_cookies, token_0, token_1):
    # Crear un administrador de conexiones
    http = urllib3.PoolManager()

    # Realizar la solicitud GET sin enviar cookies
    response = http.request(
        'GET',
        api_url,
        headers={
            'Host': 'www.hedra.com',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'Content-Type': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.hedra.com/login?redirectUrl=%2F&ref=nav',
            'Accept-Language': 'es-ES,es;q=0.9',
            "Cookie": f"{formatted_cookies}; __Secure-next-auth.session-token.0={token_0}; __Secure-next-auth.session-token.1={token_1}",
            "Accept-Encoding": "gzip, deflate"
        }
    )

    data = json.loads(response.data.decode('utf-8'))

    print("accessToken: ",data)

    # Extraer el access_token
    access_token = data.get('user', {}).get('access_token', None)
    print(access_token)
    return response.status, access_token


def obtener_session(url, token_0, token_1, csrf_Cookies):
    """
    Realiza una solicitud GET al endpoint /api/auth/session y devuelve el accessToken.

    Args:
        url (str): La URL completa para la solicitud.
        token_0 (str): Token de sesión 0.
        token_1 (str): Token de sesión 1.
        csrf_Cookies (str): CSRF token.

    Returns:
        str: El accessToken si la solicitud es exitosa o un mensaje de error.
    """
    # Definir los headers
    headers = {
        'Host': 'www.hedra.com',
        'Connection': 'keep-alive',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Content-Type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.hedra.com/login?redirectUrl=%2Fapp%2Fcharacters&ref=nav',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Cookie': f'__Host-next-auth.csrf-token={csrf_Cookies}; ph_phc_LPkfNqgrjYQMX7vjw63IAdpzDFpLNUz4fSq3dgbMRgS_posthog=%7B%22distinct_id%22%3A%2201934817-cd5b-7047-a6af-305be15c4375%22%2C%22%24sesid%22%3A%5B1732081356507%2C%2201934817-cd5a-7c5d-8fc2-dd035afbbe99%22%2C1732081339738%5D%7D; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.hedra.com%2Flogin%3FredirectUrl%3D%252Fapp%252Fcharacters%26ref%3Dnav; __Secure-next-auth.session-token.0={token_0}; __Secure-next-auth.session-token.1={token_1}',
        'Accept-Encoding': 'gzip, deflate',
    }

    # Realizar la solicitud GET
    try:
        response = requests.get(url, headers=headers)

        # Verificar el estado de la respuesta
        if response.status_code == 200:
            data = response.json()  # Convertir la respuesta a JSON
            # Extraer el accessToken
            access_token = data.get('user', {}).get('accessToken', None)

            if access_token:
                print("Registro completo")
                return access_token  # Retornar el accessToken
            else:
                return "AccessToken no encontrado en la respuesta."
        else:
            return f"Error en la solicitud: {response.status_code}"
    except Exception as e:
        return f"Error al realizar la solicitud: {str(e)}"



def post_sign_in(txtCorreo, txtContra, formatted_cookies, session_token, csrf_token):
    url = "https://www.hedra.com/api/auth/callback/credentials"
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "Content-Type": "application/x-www-form-urlencoded",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": f"{formatted_cookies}; ph_phc_LPkfNqgrjYQMX7vjw63IAdpzDFpLNUz4fSq3dgbMRgS_posthog=%7B%22distinct_id%22%3A%22d8712390-0001-7079-897e-1eb6d2aa371d%22%2C%22%24sesid%22%3A%5B1723321702013%2C%2201913dfa-5168-7dea-8e61-d31f9f65d4ca%22%2C1723321700712%5D%2C%22%24epp%22%3Atrue%7D; __Secure-next-auth.session-token={session_token}",
        "Accept-Encoding": "gzip, deflate"
    }

    data = {
        "email": f"{txtCorreo}",
        "password": f"{txtContra}",
        "action": "signIn",
        "redirect": "false",
        "csrfToken": f"{csrf_token}",
        "callbackUrl": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "json": "true"
    }

    encoded_data = urlencode(data)

    http = urllib3.PoolManager()
    try:
        response = http.request(
            'POST',
            url,
            body=encoded_data,
            headers=headers
        )
    except Exception as e:
        print(f"Error during request: {e}")
        return None, None

    if response.status == 200:
        if 'set-cookie' in response.headers:
            cookies = response.headers['set-cookie']
            print("Cookies recibidas:")
            #print(cookies)

            # Extracción de los valores de las cookies específicas
            session_token_0 = None
            session_token_1 = None

            # Buscar los tokens específicos en las cookies
            match_0 = re.search(r'__Secure-next-auth.session-token.0=([^;]+)', cookies)
            match_1 = re.search(r'__Secure-next-auth.session-token.1=([^;]+)', cookies)

            if match_0:
                session_token_0 = match_0.group(1)
            if match_1:
                session_token_1 = match_1.group(1)

            # Imprimir los valores extraídos
            #if session_token_0:
             #   print(f"__Secure-next-auth.session-token.0: {session_token_0}")
            #if session_token_1:
            #    print(f"__Secure-next-auth.session-token.1: {session_token_1}")

            # Retornar los tokens extraídos
            return session_token_0, session_token_1
        else:
            print("No se encontraron cookies en la respuesta.")
            return None, None
    else:
        print(f"Failed to post credentials. Status code: {response.status}")
        return None, None


def get_session_info():
    url = "https://www.hedra.com/api/auth/csrf"
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/login?redirectUrl=%2F&ref=nav",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        print("Response received:")
        #print(response.json())  # Cambia a response.text si no es JSON

        # Extraer y formatear las cookies
        cookies = response.cookies
        formatted_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])

        print("Formatted Cookies:")
        print(formatted_cookies)

        # Retornar el csrfToken y las cookies formateadas si deseas utilizarlas después
        csrf_token = response.json().get('csrfToken')
        return csrf_token, formatted_cookies

    except requests.exceptions.RequestException as e:
        print(f"Failed to get session info. Error: {e}")

