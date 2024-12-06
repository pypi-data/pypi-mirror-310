import subprocess
import os

def extraer_ultimo_fotograma_ffmpeg(ruta_video, ruta_imagen):
    """
    Extrae el último fotograma de un video usando FFmpeg y lo guarda
    en la ruta especificada, reemplazando el archivo si ya existe.

    Args:
        ruta_video: Ruta al archivo de video.
        ruta_imagen: Ruta donde se guardará la imagen (incluyendo extensión).
    """
    # Verifica si el archivo ya existe y lo elimina si es necesario
    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)

    # Obtiene la duración del video
    duracion_cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        ruta_video
    ]
    duracion = float(subprocess.check_output(duracion_cmd))

    # Calcula el tiempo para buscar cerca del final (0.1 segundos antes)
    tiempo_busqueda = str(duracion - 0.1)

    # Construye el comando FFmpeg para extraer el último fotograma
    comando = [
        "ffmpeg",
        "-ss", tiempo_busqueda,  # Busca cerca del final
        "-i", ruta_video,
        "-vframes", "1",  # Extrae solo un fotograma
        "-qscale:v", "2",  # Ajusta la calidad si es necesario
        ruta_imagen
    ]

    # Ejecuta el comando FFmpeg
    subprocess.run(comando)

def extraer__fotograma():
# Ejemplo de uso
  video_path = '/tmp/rt32gaarfcaghattasc/videotovideo.mp4'
  output_image_path = '/tmp/img_fragmento.jpg'
  extraer_ultimo_fotograma_ffmpeg(video_path, output_image_path)