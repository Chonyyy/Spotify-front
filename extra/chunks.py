import json
from mutagen.mp3 import MP3
import os

def split_audio_file(file_path, chunk_size_bytes=1024*50): 
    try:
        audio = MP3(file_path)# Abrir el archivo MP3
        total_size = os.path.getsize(file_path) # Obtener el tamaño total del archivo
        
        # Preparar el directorio para los chunks
        chunks_dir = f"{os.path.splitext(file_path)[0]}_chunks"
        os.makedirs(chunks_dir, exist_ok=True)
        
        # Variable para contar los chunks
        chunk_count = 0
        
        # Abrir el archivo original en modo binario
        with open(file_path, 'rb') as src:

            # Resto del archivo
            remaining_size = total_size
            
            # Dividir el resto del archivo en chunks
            current_offset = audio.info.length
            while remaining_size > 0:
                chunk_content = src.read(min(chunk_size_bytes, remaining_size))
                chunk_filename = os.path.join(chunks_dir, f'chunk_{chunk_count+1}.mp3')
                
                # Escribir el contenido del chunk
                with open(chunk_filename, 'wb') as dst:
                    dst.write(chunk_content)
                
                remaining_size -= len(chunk_content)
                chunk_count += 1
        
        return [f"{chunks_dir}/chunk_{i}.mp3" for i in range(chunk_count)]
    
    except Exception as e:
        print(f"Error al dividir la canción: {str(e)}")
        return None


def create_json_chunks(chunks, file_path):
    json_data = {
        "filename": file_path,
        "chunks": chunks
    }
    return json_data


def save_to_json(json_data, output_file):
    with open(output_file, 'w') as f:
        json.dump(json_data, f, indent=2)

def main():
    all_chunks_songs = []
    # for song in [f for f in os.listdir("/home/chony/Escritorio/Spotify/music") if f.lower().endswith(('.mp3', '.mpeg'))]:
    #     file_path = f"/home/chony/Escritorio/Spotify/music/{song}"
    for song in [f for f in os.listdir("C:\\Users\\Chony\\Desktop\\Spotify-front\\music") if f.lower().endswith(('.mp3', '.m4a'))]:
        file_path = f"C:\\Users\\Chony\\Desktop\\Spotify-front\music\\{song}"
        chunks = split_audio_file(file_path)
        json_data = create_json_chunks(chunks, file_path)
        all_chunks_songs.append(json_data)
        
        print(f"Archivo '{file_path}' dividido en {len(chunks)} chunks y guardado en {os.path.splitext(file_path)[0]}_chunks.json.")
    
    json = {
        "songs_by_chunks": all_chunks_songs
        }
    
    save_to_json(json, f"chunks.json")
    
if __name__ == "__main__":
    main()