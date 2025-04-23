import requests
import pandas as pd
import time
import random
from datetime import datetime
from urllib.parse import urlparse

# ===== CONFIGURACIÓN =====
CONFIG = {
    "POST_URL": "https://www.tiktok.com/@labicolor_pe/video/7424737284664184070",  # URL del video
    "MS_TOKEN": "TU_MS_TOKEN_ACTUAL",                                             # Token msToken
    "X_BOGUS": "TU_X_BOGUS_ACTUAL",                                               # Token X-Bogus
    "WEB_ID": "7478343844027729413",                                              # Web ID de la cookie
    "MAX_RETRIES": 3,                                                             # Reintentos por fallo
    "DELAY_BETWEEN_REQUESTS": 1.5,                                                # Delay entre peticiones (segundos)
    "MAX_COMMENTS": 10000,                                                        # Límite de comentarios
    "OUTPUT_FORMATS": ["csv", "json"],                                            # Formatos de salida
    "USER_AGENTS": [                                                              # User-Agents para rotación
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1'
    ]
}

# ===== FUNCIONES AUXILIARES =====
def extract_video_id(url: str) -> str:
    """Extrae el ID del video de la URL."""
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    if 'video' not in path_parts:
        raise ValueError("URL no válida: debe contener '/video/'.")
    video_id = path_parts[path_parts.index('video') + 1]
    return video_id.split('?')[0]  # Elimina parámetros adicionales

def format_timestamp(timestamp: int) -> str:
    """Convierte un timestamp Unix a una fecha legible."""
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "Fecha no disponible"

def get_random_user_agent() -> str:
    """Devuelve un User-Agent aleatorio de la lista."""
    return random.choice(CONFIG["USER_AGENTS"])

def get_headers(username: str) -> dict:
    """Genera los headers para la petición API."""
    return {
        'authority': 'www.tiktok.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': f'https://www.tiktok.com/@{username}',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': get_random_user_agent(),
        'cookie': f'tt_webid_v2={CONFIG["WEB_ID"]}; tt_webid={CONFIG["WEB_ID"]}; msToken={CONFIG["MS_TOKEN"]}'
    }

# ===== FUNCIONES PRINCIPALES =====
def make_api_request(video_id: str, cursor: int, username: str, retry_count: int = 0) -> dict:
    """Realiza una petición a la API de TikTok."""
    params = {
        'aid': 1988,
        'aweme_id': video_id,
        'cursor': cursor,
        'count': 20,
        'web_id': CONFIG["WEB_ID"],
        'msToken': CONFIG["MS_TOKEN"],
        'X-Bogus': CONFIG["X_BOGUS"]
    }
    
    try:
        response = requests.get(
            'https://www.tiktok.com/api/comment/list/',
            headers=get_headers(username),
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if retry_count < CONFIG["MAX_RETRIES"]:
            wait_time = CONFIG["DELAY_BETWEEN_REQUESTS"] * (retry_count + 1)
            print(f"Error en la petición (reintento {retry_count + 1}): {str(e)} - Esperando {wait_time} segundos")
            time.sleep(wait_time)
            return make_api_request(video_id, cursor, username, retry_count + 1)
        print(f"Error definitivo en la petición: {str(e)}")
        return None

def parse_comments(api_data: dict, current_cursor: int) -> dict:
    """Procesa los comentarios de la respuesta API y devuelve solo los campos solicitados."""
    if not api_data or not api_data.get('comments'):
        return None
        
    parsed_comments = []
    for comment in api_data['comments']:
        try:
            parsed_comments.append({
                'user': comment['user']['nickname'],
                'comment': comment.get('text', '') or comment.get('share_info', {}).get('desc', ''),
                'time': format_timestamp(comment.get('create_time', '')),
                'likes': comment.get('digg_count', 0),
                'reply_count': comment.get('reply_comment_total', 0)
            })
        except KeyError as e:
            print(f"Error procesando comentario: {str(e)} - Comentario omitido")
    
    return {
        'comments': parsed_comments,
        'has_more': api_data.get('has_more', 0),
        'cursor': api_data.get('cursor', current_cursor + 20)
    }

def save_data(data: list, video_id: str, suffix: str = "final") -> None:
    """Guarda los datos en CSV y JSON."""
    df = pd.DataFrame(data)
    for fmt in CONFIG["OUTPUT_FORMATS"]:
        filename = f'tiktok_comments_{video_id}_{suffix}.{fmt}'
        try:
            if fmt == 'csv':
                df.to_csv(filename, index=False, encoding='utf-8')
            else:
                df.to_json(filename, orient='records', indent=4, force_ascii=False)
            print(f" Datos guardados: {filename}")
        except Exception as e:
            print(f"Error al guardar {fmt}: {str(e)}")

# ===== EJECUCIÓN PRINCIPAL =====
def main():
    try:
        # Extraer información de la URL
        video_id = extract_video_id(CONFIG["POST_URL"])
        username = CONFIG["POST_URL"].split('@')[1].split('/')[0]
        
        print(f"\n=== Iniciando extracción de comentarios ===")
        print(f" Video ID: {video_id}")
        print(f" Usuario: @{username}")
        print(f" URL: {CONFIG['POST_URL']}\n")
        
        all_comments = []
        cursor = 0
        has_more = True
        
        while has_more and len(all_comments) < CONFIG["MAX_COMMENTS"]:
            # Petición a la API
            api_data = make_api_request(video_id, cursor, username)
            if not api_data:
                break
                
            # Procesar comentarios
            parsed_data = parse_comments(api_data, cursor)
            if not parsed_data or not parsed_data['comments']:
                break
                
            all_comments.extend(parsed_data['comments'])
            cursor = parsed_data['cursor']
            has_more = parsed_data['has_more'] == 1
            
            print(f" Comentarios obtenidos: {len(all_comments)} | Cursor: {cursor}")
            
            # Guardar progreso parcial cada 100 comentarios
            if len(all_comments) % 100 == 0:
                save_data(all_comments, video_id, "partial")
            
            # Delay aleatorio para evitar bloqueos
            time.sleep(CONFIG["DELAY_BETWEEN_REQUESTS"] + random.uniform(0, 1))
            
    except KeyboardInterrupt:
        print("\n¡Extracción detenida manualmente!")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
    finally:
        if all_comments:
            save_data(all_comments, video_id, "final")
            print(f"\n=== Resumen ===")
            print(f" Total de comentarios: {len(all_comments)}")
        else:
            print("\nNo se extrajeron comentarios.")

if __name__ == "__main__":
    main()