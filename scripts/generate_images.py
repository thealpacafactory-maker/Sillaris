import os
import json
import time
import urllib.request
import urllib.error

# Configuración de KIE.AI
API_KEY = "f3d35049befcd91e0611b67a733f9733"
BASE_URL = "https://api.kie.ai"
MODEL_NAME = "gpt-image-2-text-to-image"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "images")

# Definición de las imágenes a generar con los IDs de las tareas ya creadas para ahorrar créditos
IMAGES_TO_GENERATE = [
    {
        "filename": "hero-main.webp",
        "aspect_ratio": "4:5",
        "resolution": "1K",  # Cambiado a 1K para evitar 'Internal Error' en KIE.AI
        "prompt": "High-end 10-story modern corporate building facade in Parque Industrial Arequipa, sleek dark blue glass panels and polished gray concrete pillars, green pocket gardens on balconies, bright clear blue sky, soft morning sunlight, architectural photography, photorealistic, ultra-detailed, 8k",
        "cached_task_id": None # Falló anteriormente, se reintentará
    },
    {
        "filename": "why-sillaris.webp",
        "aspect_ratio": "3:4",
        "resolution": "2K",
        "prompt": "Medium-shot of a professional Peruvian real estate advisor in a smart casual business outfit showing plans on a tablet to a young couple. They are sitting at a wooden table on a sunny modern rooftop terrace in Yanahuara, Arequipa. Traditional white volcanic sillar stone walls in the background, warm light, natural expressions, high fidelity, 8k",
        "cached_task_id": "c30b35c77ea292efcde592671957f821"
    },
    {
        "filename": "prop_vucetich_main.webp",
        "aspect_ratio": "4:3",
        "resolution": "2K",
        "prompt": "Modern exterior shot of the Vucetich corporate building in Arequipa. 10 stories of polished dark gray concrete and clean glass panels, pristine street view with green trees, bright daylight, photorealistic architectural render, 8k",
        "cached_task_id": "c9e6d3094dc31b90627c87a04a1d5e85"
    },
    {
        "filename": "prop_umacollo_main.webp",
        "aspect_ratio": "4:3",
        "resolution": "2K",
        "prompt": "Interior design of a cozy 35sqm studio apartment in Umacollo, Yanahuara, Arequipa. Modern Scandinavian style, minimalist open-concept kitchenette with light wood cabinets, small dining bar, balcony window showing bright daylight, photorealistic",
        "cached_task_id": "e4c664804edcb9d99c054159c5c50593"
    },
    {
        "filename": "prop_vallejo35_main.webp",
        "aspect_ratio": "4:3",
        "resolution": "2K",
        "prompt": "3D architectural render of a modern 35sqm one-bedroom flat interior in Arequipa. Sleek kitchen island with white quartz countertop, light beige sofa, contemporary lighting, clean minimalist design, warm natural light, high-end visualization",
        "cached_task_id": "1b9906823d3e6377f9ff584ce31bfb64"
    },
    {
        "filename": "prop_vallejo65_main.webp",
        "aspect_ratio": "4:3",
        "resolution": "2K",
        "prompt": "3D architectural render of a modern family living room and integrated dining space, 65sqm layout. Wooden dining table for four, comfortable beige fabric sofa, large glass sliding doors leading to a balcony, natural bright light, elegant interior",
        "cached_task_id": "5d40ace3da021507365e8998caae3187"
    },
    {
        "filename": "prop_vallejo85_main.webp",
        "aspect_ratio": "4:3",
        "resolution": "2K",
        "prompt": "3D architectural render of a premium 85sqm apartment living room. Large sand-colored sectional sofa, elegant dining table for six, wide balcony terrace with beautiful green potted plants, sophisticated lighting, high-end warm finishes",
        "cached_task_id": "15f0e886b9c3ecb00f5ce00020ffb96f"
    },
    {
        "filename": "prop_local_vallejo_main.webp",
        "aspect_ratio": "4:3",
        "resolution": "2K",
        "prompt": "Modern retail commercial storefront space on the ground floor of a contemporary residential building. Large floor-to-ceiling glass display windows with warm interior boutique lighting, elegant signage, clean sidewalk view, high visibility",
        "cached_task_id": "a3c9605c88757d60b50bb584e8020347"
    },
    {
        "filename": "prop_casa_negrita_main.webp",
        "aspect_ratio": "4:3",
        "resolution": "2K",
        "prompt": "Exterior facade of a large modern corporate house in La Negrita, Arequipa. Designed for office use, double-story, white volcanic sillar stone details, parking area with three modern cars, neat front garden, clear sunny day",
        "cached_task_id": "632f13981eeae8f603e820f79c626065"
    },
    {
        "filename": "prop_casa_ugarte_main.webp",
        "aspect_ratio": "4:3",
        "resolution": "2K",
        "prompt": "Imposing commercial showroom facade of a double-story property on Alfonso Ugarte Avenue in Arequipa. Large storefront display windows, modern clean sidewalk, bright sunny day, spaces for corporate logo signage, high visibility",
        "cached_task_id": "978328f07e9ce93468325cf0b5ea52fd"
    },
    {
        "filename": "blog_guia_comprar.webp",
        "aspect_ratio": "16:9",
        "resolution": "2K",
        "prompt": "A aesthetic composition representing home ownership: a set of house keys on a wooden keychain next to a warm cup of coffee on a light oak wooden desk. Soft out-of-focus background of a window showing a bright blue sky, cozy morning lighting",
        "cached_task_id": None
    },
    {
        "filename": "blog_mejores_zonas.webp",
        "aspect_ratio": "16:9",
        "resolution": "2K",
        "prompt": "Beautiful scenic view of Yanahuara traditional neighborhood in Arequipa. Narrow stone-paved street with white volcanic sillar stone arches and houses, red geranium flowers in clay pots, majestic snow-capped Misti volcano in the background under clear blue sky, photorealistic",
        "cached_task_id": None
    }
]

def make_request(url, method="GET", data=None, headers=None):
    """Realiza una petición HTTP utilizando la librería estándar de Python."""
    if headers is None:
        headers = {}
    
    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    
    headers["Authorization"] = f"Bearer {API_KEY}"
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"\n[ERROR HTTP {e.code}]: {error_body}")
        try:
            return json.loads(error_body)
        except Exception:
            return {"code": e.code, "msg": str(e), "data": None}
    except Exception as e:
        print(f"\n[ERROR CONEXIÓN]: {e}")
        return {"code": 500, "msg": str(e), "data": None}

def find_url(obj):
    """Busca de manera recursiva cualquier clave en el JSON que contenga una URL de imagen válida."""
    if isinstance(obj, str):
        # Primero verificar si es un string JSON que podemos decodificar (como resultJson)
        stripped = obj.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            try:
                parsed = json.loads(obj)
                res = find_url(parsed)
                if res:
                    return res
            except Exception:
                pass
        
        # Validar si es una URL de imagen
        if obj.startswith("http") and any(obj.lower().split("?")[0].endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
            return obj
        # Respaldo: Si parece una url absoluta de cdn/archivo pero no termina en extensión conocida
        if obj.startswith("http") and ("kie-ai" in obj or "cdn" in obj or "assets" in obj or "tempfile" in obj):
            return obj
            
    elif isinstance(obj, dict):
        # Primero buscar llaves comunes como resultImageUrl, imageUrl, outputUrl, url, resultUrls
        for key in ["resultImageUrl", "imageUrl", "outputUrl", "url", "result", "resultUrls"]:
            if key in obj:
                val = obj[key]
                if isinstance(val, str) and val.startswith("http"):
                    return val
                elif isinstance(val, list):
                    for item in val:
                        if isinstance(item, str) and item.startswith("http"):
                            return item
        # Búsqueda recursiva en todo el diccionario
        for k, v in obj.items():
            res = find_url(v)
            if res:
                return res
    elif isinstance(obj, list):
        for item in obj:
            res = find_url(item)
            if res:
                return res
    return None

def download_image(url, filepath):
    """Descarga la imagen desde la URL con cabeceras de navegador reales para evitar HTTP 403 Forbidden."""
    print(f" -> Descargando imagen a: {filepath} ...")
    try:
        # Simulamos un agente de navegación real (Chrome) para evitar bloqueos del CDN
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Referer': 'https://kie.ai/'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as out_file:
                while True:
                    chunk = response.read(16384) # 16KB chunks
                    if not chunk:
                        break
                    out_file.write(chunk)
                    
        print(" -> [ÉXITO] Imagen guardada correctamente.")
        return True
    except Exception as e:
        print(f" -> [ERROR AL DESCARGAR]: {e}")
        return False

def generate_image_task(img_config):
    """Crea una tarea de generación en KIE.AI (o recupera una existente) y descarga el resultado."""
    print(f"\n==================================================")
    print(f"PROCESANDO: {img_config['filename']}")
    print(f"Aspect Ratio: {img_config['aspect_ratio']} | Resolution: {img_config['resolution']}")
    print(f"Prompt: {img_config['prompt'][:60]}...")
    print(f"==================================================")
    
    task_id = img_config.get("cached_task_id")
    
    if task_id:
        print(f" -> [CACHÉ] Usando Task ID de la corrida anterior para ahorrar créditos: {task_id}")
    else:
        # 1. Crear la tarea si no hay ID guardado
        create_url = f"{BASE_URL}/api/v1/jobs/createTask"
        payload = {
            "model": MODEL_NAME,
            "input": {
                "prompt": img_config["prompt"],
                "aspect_ratio": img_config["aspect_ratio"],
                "resolution": img_config["resolution"]
            }
        }
        
        print(" -> Enviando petición de creación de tarea...")
        res = make_request(create_url, method="POST", data=payload)
        
        if not res or res.get("code") != 200:
            print(f" -> [FALLÓ CREACIÓN]: {res.get('msg', 'Error desconocido')}")
            return False
        
        task_id = res.get("data", {}).get("taskId")
        if not task_id:
            print(" -> [FALLÓ CREACIÓN]: No se recibió el taskId de KIE.AI.")
            return False
            
        print(f" -> [CREADA] Task ID: {task_id}")
    
    # 2. Pollear la tarea (o consultar el estado del caché)
    poll_url = f"{BASE_URL}/api/v1/jobs/recordInfo?taskId={task_id}"
    max_attempts = 40  # 40 * 5s = 200 segundos máximo por imagen
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f" -> Consultando estado (Intento {attempt}/{max_attempts})...", end="", flush=True)
        
        status_res = make_request(poll_url, method="GET")
        if not status_res or status_res.get("code") != 200:
            print(f" Error en consulta: {status_res.get('msg', 'Desconocido')}")
            time.sleep(5)
            continue
            
        data = status_res.get("data", {})
        # Soportamos tanto 'state' como 'status' para máxima compatibilidad
        state = (data.get("state") or data.get("status") or "").lower()
        print(f" Estado actual: {state.upper()}")
        
        if state in ["success", "completed", "successful"]:
            # Buscar la URL de la imagen en la respuesta
            img_url = find_url(data)
            if img_url:
                print(f" -> [LOGRADO] URL de imagen encontrada: {img_url}")
                # Crear ruta de guardado
                filepath = os.path.join(OUTPUT_DIR, img_config["filename"])
                return download_image(img_url, filepath)
            else:
                print(" -> [ERROR]: Tarea completada con éxito pero no se encontró ninguna URL de imagen en el JSON:")
                print(json.dumps(data, indent=2))
                return False
                
        elif state in ["fail", "failed", "error"]:
            fail_detail = data.get("failMsg") or data.get("failCode") or "Sin detalles de error"
            print(f" -> [ERROR]: La generación falló. Mensaje KIE: {status_res.get('msg')} | Detalle: {fail_detail}")
            return False
            
        # Si sigue esperando, en cola o procesando, esperamos 5 segundos
        time.sleep(5)
        
    print(" -> [TIEMPO AGOTADO]: La tarea tardó demasiado en completarse.")
    return False

def main():
    print("INICIANDO GENERACIÓN DE IMÁGENES CON KIE.AI (Modelo GPT Image 2)")
    print(f"Directorio de salida: {OUTPUT_DIR}\n")
    
    start_time = time.time()
    success_count = 0
    
    for img_config in IMAGES_TO_GENERATE:
        # Si la imagen ya fue descargada y existe físicamente en el disco, la omitimos
        filepath = os.path.join(OUTPUT_DIR, img_config["filename"])
        if os.path.exists(filepath):
            print(f"\n[OMITIDO]: {img_config['filename']} ya existe localmente en el disco.")
            success_count += 1
            continue
            
        # Añadimos un pequeño delay preventivo entre creaciones
        time.sleep(2)
        if generate_image_task(img_config):
            success_count += 1
        else:
            print(f" -> No se pudo generar la imagen {img_config['filename']}")
            
    end_time = time.time()
    elapsed = end_time - start_time
    
    print("\n==================================================")
    print("PROCESO TERMINADO")
    print(f"Imágenes guardadas con éxito: {success_count} / {len(IMAGES_TO_GENERATE)}")
    print(f"Tiempo transcurrido: {elapsed:.1f} segundos")
    print("==================================================")

if __name__ == "__main__":
    main()
