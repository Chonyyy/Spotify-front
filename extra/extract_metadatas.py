import os
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, ID3NoHeaderError
from mutagen.mp4 import MP4

# Ruta del directorio con los archivos MP3 y M4A
directory_path = '../music'

def extract_cover_image(audio_file_path):
    """Extrae la imagen de portada de un archivo MP3 o M4A y la devuelve como datos binarios."""
    try:
        if audio_file_path.lower().endswith('.mp3'):
            audio = MP3(audio_file_path, ID3=ID3)
            tags = audio.tags
            if tags:
                for tag in tags.values():
                    if isinstance(tag, APIC):
                        return tag.data
        elif audio_file_path.lower().endswith('.m4a'):
            audio = MP4(audio_file_path)
            if 'covr' in audio:
                return audio['covr'][0]
        return None
    except ID3NoHeaderError:
        print(f'No se encontraron metadatos ID3 en {audio_file_path}.')
        return None
    except Exception as e:
        print(f'Error al procesar {audio_file_path}: {e}')
        return None

def get_metadata(audio_file_path):
    """Obtiene los metadatos de un archivo MP3 o M4A y la imagen de portada, si está disponible."""
    try:
        if audio_file_path.lower().endswith('.mp3'):
            audio = MP3(audio_file_path, ID3=ID3)
            metadata = {
                "id": 1,  # Puedes asignar un ID único si es necesario
                "title": audio.get('TIT2', [None])[0],
                "artist": audio.get('TPE1', [None])[0],
                "genre": audio.get('TCON', [None])[0],
                "album": audio.get('TALB', [None])[0],
                "address": audio_file_path,
                "img": None
            }
        elif audio_file_path.lower().endswith('.m4a'):
            audio = MP4(audio_file_path)
            metadata = {
                "id": 1,  # Puedes asignar un ID único si es necesario
                "title": audio.tags.get('\xa9nam', [None])[0],
                "artist": audio.tags.get('\xa9ART', [None])[0],
                "genre": audio.tags.get('\xa9gen', [None])[0],
                "album": audio.tags.get('\xa9alb', [None])[0],
                "address": audio_file_path,
                "img": None
            }

        # Extraer la imagen de portada
        cover_data = extract_cover_image(audio_file_path)
        if cover_data:
            cover_image_path = os.path.join(directory_path, f'{os.path.splitext(os.path.basename(audio_file_path))[0]}_cover.jpg')
            with open(cover_image_path, 'wb') as img_file:
                img_file.write(cover_data)
            metadata["img"] = cover_image_path

        return metadata

    except Exception as e:
        print(f'Error al obtener metadatos de {audio_file_path}: {e}')
        return None

def process_directory(directory_path):
    """Itera por todos los archivos MP3 y M4A en el directorio, obtiene los metadatos y guarda la información en un diccionario."""
    all_metadata = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.mp3', '.m4a')):
            audio_file_path = os.path.join(directory_path, filename)
            metadata = get_metadata(audio_file_path)
            if metadata:
                all_metadata.append(metadata)
    
    # Guardar la información en un archivo JSON
    with open('metadata.json', 'w') as json_file:
        json.dump(all_metadata, json_file, indent=4)

    print('Metadatos guardados en metadata.json')

# Llamar a la función para procesar el directorio
process_directory(directory_path)
