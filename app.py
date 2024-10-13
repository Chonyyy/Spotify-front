from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import time, requests, socket, logging, hashlib, threading, base64
from fastapi import FastAPI
from discovery import discover_gateway  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
logger = logging.getLogger("__main__")

logging.basicConfig(
    filename= f'logs.log',
    filemode= 'w')

logger.setLevel(logging.DEBUG)# TODO: Set this from input

File

# Modelos de datos
class Song(BaseModel):
    # id: int
    title: str
    artist: str
    genre: str
    album: str
    # address: str
    # img: str
    
songs = [
    {
        "id": 1, 
        "title": "Sustem of a down – Toxicity.mp3", 
        "artist": "Sustem of a down",
        "genre":"rock", 
        "album":"lal", 
        "address":"music/Sustem of a down – Toxicity.mp3", 
        "img":"music/sleep-token-aqua-regia_cover.jpg"
    }
]

BaseUrl = 'http://localhost:8002/gw'

def get_leader_url():
    gateway_ip = discover_gateway()
    if not gateway_ip:
        raise HTTPException(status_code=500, detail="No se pudo encontrar el gateway líder")
    return f'http://{gateway_ip}:8001/gw'

@app.get("/get-songs", response_model=List[Song])
def get_songs(limit: int = 4, offset: int = 0):
    base_url = get_leader_url() 
    logger.info("url " + f'{base_url}/get-songs')
    response = requests.get(f'{base_url}/get-songs')
    logger.info(f'response \n {response}')
    data = response.json()
    return data
    # return songs[offset:offset + limit]

@app.post("/save-song")
def save_song(
        file: UploadFile = File(...),
        title: str = Form(...),
        artist: str = Form(...),
        album: str = Form(...),
        genre: str = Form(...)
    ):
    base_url = get_leader_url() 
    logger.info(f'Storing song {title}')
    response = requests.post(f'{base_url}/store-song-file', json={'title': title, 'genre': genre, 'album': album, 'artist':artist})

    # Recibir IP y puerto del socket
    socket_info = response.json()  
    ip = socket_info.get('ip')
    port = socket_info.get('port')

    if not ip or not port:
        return JSONResponse(content={'status': 'error', 'message': 'No se recibió información del socket'}, status_code=500)
    
    logger.info(f'Socket received: {ip}:{port}')
    # Enviar archivo en chunks de 1024 bytes al socket de uno en uno
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect((ip, port))  # Conectar al socket
            chunk_size = 50000  # Tamaño del chunk en bytes
            
            # Leer el archivo por chunks y enviar de uno en uno
            while True:
                chunk = file.file.read(chunk_size)
                if not chunk:
                    break
                logger.info(f'Sending chunk {chunk}')
                sock.send(chunk)  # Enviar el chunk individual
                logger.info(f'Sent chunk of size {len(chunk)} bytes to {ip}:{port}')
                # Esperar un poco entre envíos si es necesario
                time.sleep(0.1)  # Ajusta este tiempo según sea necesario
                
        return {'status': 'success'}
    
    except Exception as e:
        logger.error(f'Error sending file chunks: {e}')
        return JSONResponse(content={'status': 'error', 'message': 'Error al enviar el archivo'}, status_code=500)

@app.post("/get-song-file")
def get_song_file(title, artist, album):
    key = get_sha_repr(title + artist + album)
    base_url = get_leader_url() 
    logger.info(f'Getting song {title}')

    socket_ip, socket_port = _create_udp_socket()
    file_transfer_thread = threading.Thread(target=_receive_file_data, args=(socket_ip, title), daemon=True)
    file_transfer_thread.start()

    response = requests.get(f'{base_url}/get-song-file', json={'song_key': key, 'udp_ip': socket_ip, 'udp_port': socket_port, 'start_chunk':0})
    while file_transfer_thread.is_alive():
        time.sleep(1)
    
    data = response.json()
    return data


@app.get("/get-songs-by-title/{song_title}")
def get_songs_by_title(song_title: str):
    base_url = get_leader_url() 
    logger.info(f'song title {song_title}')
    
    response = requests.post(f'{base_url}/get-songs-by-title', json = {"title": song_title})
    result = []
    for item in response.json():
        result.append({
            'title': item['title'],
            'artist': item['artist'],
            'genre': item['genre'],
            'album': item['album'],
        })
    return result

@app.get("/get-songs-by-genre/{genre}")
def get_songs_by_genre(genre: str, limit: int = 4, offset: int = 0):
    base_url = get_leader_url() 
    logger.info(f'genre {genre}')
    response = requests.post(f'{base_url}/get-songs-by-genre', json = {'genre': genre})
    result = []
    for item in response.json():
        result.append({
            'title': item['title'],
            'artist': item['artist'],
            'genre': item['genre'],
            'album': item['album'],
        })
    logger.info(f'response get song genre {response.content}')

    if not response:
        raise HTTPException(status_code=404, detail="No songs found for the specified genre")
    return result
    # return response[offset:offset + limit]

@app.post("/get-songs-by-artist/{artist}") #TODO Hacer esto en el back
def get_songs_by_artist(artist: str, limit: int = 4, offset: int = 0):
    base_url = get_leader_url() 
    response = requests.post(f'{base_url}/get-songs-by-artist', json = {'artist': artist})
    
    if not response:
        raise HTTPException(status_code=404, detail="No songs found for the specified artist")
    return response

def get_sha_repr(data: str) -> int:
    """Return SHA-1 hash representation of a string as an integer."""
    return int(hashlib.sha1(data.encode()).hexdigest(), 16)

def _create_udp_socket():
        """
        Create and bind a UDP socket to an available port.
        Returns:
            udp_socket: The UDP socket object.
            port (int): The port number the socket is bound to.
        """
        ip = socket.gethostbyname(socket.gethostbyname())
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((ip, 0))  # Bind to any available port
        port = udp_socket.getsockname()[1]
        logger.info(f"UDP socket created at {ip}:{port}")
        return udp_socket, port

def _receive_file_data(udp_socket, song_title: str):
        """
        Receive file data over the UDP socket and send it to storage_services.
        Args:
            udp_socket: The UDP socket object.
            file_id (str): Identifier for the file being received.
        """
        try:
            logger.info(f"Listening for file data on UDP socket for file ID: {song_title}")
            start = 0
            chunk_num = 0
            while True:
                file_data = bytearray()  # Use bytearray to accumulate binary file data
                data, addr = udp_socket.recvfrom(50000)  # Buffer size of 1024 bytes

                if data:
                    logger.info(f"Received {len(data)} bytes from {addr} via UDP")
                    bytes_decoded = base64.b64decode(data)
                    file_data.extend(bytes_decoded)  # Accumulate received data
                    # TODO comunicaarse con front y decod
                    start += 50000 #FIXME: coger el tamannno dinamicamente de data
                    chunk_num += 1
                else:
                    break
            logger.info(f"File data for {song_title} received and sended to storage services")

        except Exception as e:
            logger.error(f"Error receiving file data: {e}")

        finally:
            udp_socket.close()
            logger.info(f"UDP socket closed for file ID: {song_title}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)