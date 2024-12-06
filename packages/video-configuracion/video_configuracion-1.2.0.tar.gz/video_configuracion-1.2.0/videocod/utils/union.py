import os
import subprocess

def obtener_lista_videos(folder_path):
    """
    Obtiene una lista de archivos MP4 en el directorio especificado, ordenados por nombre.
    
    :param folder_path: Ruta de la carpeta donde están los videos
    :return: Lista de rutas a los archivos de video
    """
    videos = [os.path.join(folder_path, filename) for filename in sorted(os.listdir(folder_path)) if filename.endswith(".mp4")]
    return videos

def crear_lista_txt(folder_path, lista_txt_path):
    """
    Crea un archivo de lista de texto con las rutas a los archivos MP4 en el directorio especificado.
    
    :param folder_path: Ruta de la carpeta donde están los videos
    :param lista_txt_path: Ruta del archivo de lista de texto
    """
    videos = obtener_lista_videos(folder_path)
    with open(lista_txt_path, 'w') as f:
        for video in videos:
            f.write(f"file '{video}'\n")

def unir_videos_con_lista(lista_txt_path, output_video):
    """
    Une los videos MP4 usando un archivo de lista de texto.
    
    :param lista_txt_path: Ruta del archivo de lista de texto
    :param output_video: Ruta del archivo de video de salida
    """
    # Verifica si ffmpeg está instalado
    try:
        subprocess.run(["ffmpeg", "-version"], check=True)
    except subprocess.CalledProcessError:
        print("ffmpeg no está instalado. Debes instalarlo.")
        return
    
    # Ejecuta el comando ffmpeg para unir los videos
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
        "-i", lista_txt_path, "-c", "copy", output_video
    ]
    subprocess.run(cmd, check=True)
    print(f"Video combinado guardado en {output_video}")

def eliminar_fragmentos(folder_path):
    """
    Elimina todos los archivos en el directorio especificado.
    
    :param folder_path: Ruta de la carpeta donde están los fragmentos
    """
    for archivo in os.listdir(folder_path):
        ruta_archivo = os.path.join(folder_path, archivo)
        if os.path.isfile(ruta_archivo):
            os.remove(ruta_archivo)
    print(f"Todos los fragmentos en {folder_path} han sido eliminados.")

def uni_frag():
    # Define las rutas
    folder_path = '/tmp/rt32gaarfcaghattasc/video_output'  # Carpeta donde están los videos
    lista_txt_path = '/tmp/video_list.txt'  # Archivo de lista de texto
    video_salida = '/tmp/rt32gaarfcaghattasc/video.mp4'  # Archivo de video combinado

    # Crear el archivo de lista de texto
    crear_lista_txt(folder_path, lista_txt_path)

    # Unir los videos usando el archivo de lista de texto
    unir_videos_con_lista(lista_txt_path, video_salida)

    # Eliminar los fragmentos después de combinar los videos
    eliminar_fragmentos(folder_path)

