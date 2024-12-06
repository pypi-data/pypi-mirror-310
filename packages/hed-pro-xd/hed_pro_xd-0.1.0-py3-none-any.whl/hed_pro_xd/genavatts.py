import random
import json
import requests
from tqdm.notebook import tqdm
import time
import hashlib
import base64
from IPython.display import display, HTML
import os

def obteneravatar(access_token):
    url = "https://www.hedra.com/api/app/v1/app/projects"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/app/characters",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    response = requests.get(url, headers=headers)
    return response.json()

def eliminar_proyecto(joob_id, access_token):
    url = f"https://www.hedra.com/api/app/v1/app/projects/{joob_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.hedra.com/app/characters",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    response = requests.delete(url, headers=headers)

    # Imprime el código de estado de la respuesta y el contenido de la respuesta
    #print(f"Status Code: {response.status_code}")
    #print(f"Response: {response.text}")



def video_to_base64(video_path):
    with open(video_path, "rb") as video_file:
        video_base64 = base64.b64encode(video_file.read()).decode('utf-8')
    return video_base64

def display_video_base64(video_path):
    video_base64 = video_to_base64(video_path)
    video_html = f"""
    <video width="512" height="512" controls autoplay>
      <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    """
    display(HTML(video_html))



# Función para actualizar la barra de progreso y descargar el video si el progreso es 100%
def update_progress_bar(current_progress, ruta_video, access_token, joob_ids):
    total_steps = 100
    video_url = None
    while current_progress < 1.0:
        # Simula obtener el progreso actualizado
        response = obteneravatar(access_token)
        #print("Proceso:", response)
        project = response['projects'][0]
        current_progress = project['progress']
        video_url = project['videoUrl']  # Obtener la URL del video
        #print("Video URL:", video_url)
        
        # Calcular el contador de progreso
        step = int(current_progress * total_steps)
        
        # Imprimir el progreso en la misma línea
        print(f"\rProgreso: {step}%", end='', flush=True)
        
        time.sleep(2)  # Ajusta el intervalo de actualización aquí

    if video_url:  # Si se ha obtenido una URL del video, descarga el video
        download_video(video_url, ruta_video, access_token, joob_ids)

# Función para generar un nombre de archivo seguro a partir de una URL
def generate_safe_filename(url):
    # Usa un hash MD5 de la URL para generar un nombre de archivo único y seguro
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest() + '.mp4'

# Función para descargar el video desde una URL
def download_video(url, ruta_video, access_token, joob_ids):
    #print("url",url)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = generate_safe_filename(url)
        #print(url)
        #filename = "3424asdf.mp4"
        with open(f"{ruta_video}{filename}" , 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f" Video downloaded as {filename}")

        display_video_base64(f"{ruta_video}{filename}")

        # Ejecutar la función
        eliminar_proyecto(joob_ids, access_token)

    else:
        print("Error downloading video")

def enviar_avatar_request(text, avatar_image, aspect_ratio="16:9", prompt="", use_manual_seed=False, seed=None, voice_id="Xb7hH8MSUJpSbSDYk0k2", access_token=""):

    # Genera una semilla aleatoria si no se proporciona y si use_manual_seed es False
    if not use_manual_seed:
        seed = random.randint(1000000, 9999999)  # Genera un número aleatorio de 7 dígitos

    url = "https://www.hedra.com/api/app/v1/app/avatars/predict-async"
    headers = {
        "Host": "www.hedra.com",
        "Connection": "keep-alive",
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.hedra.com",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    # Crear el cuerpo de la solicitud
    data = {
        "text": text,
        "avatar_image": avatar_image,
        "aspect_ratio": aspect_ratio,
        "avatar_image_input": {
            "prompt": prompt,
            "seed": seed
        },
        "audio_source": "tts",  # Usando TTS como la fuente de audio
        "voice_id": voice_id
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Verificar la respuesta
    if response.status_code == 200:
        print("Request successful!")
        #print(response.json())  # Imprimir respuesta si es JSON
        # Supongamos que tienes el siguiente diccionario
        responses = response.json()

        # Extraer el job_id
        job_id = responses['job_id']
        return job_id
    else:
        print(f"Request failed with status code {response.status_code}")
        #print(response.text)
