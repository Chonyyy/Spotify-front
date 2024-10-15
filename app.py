from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse, StreamingResponse
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
    gateway_url = get_leader_url()
    listening_socket, listening_port = _create_udp_socket()
    writing_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logger.info(f'Sending song {title} to {gateway_url}')
    response = requests.post(
        f'{gateway_url}/store-song-file', 
        json=
        {
            'title': title, 
            'genre': genre, 
            'album': album, 
            'artist': artist, 
            'client_port': listening_port, 
            'client_ip': socket.gethostbyname(socket.gethostname())
        }
    )

    # Recibir IP y puerto del socket
    socket_info = response.json()  
    if not 'ip' in socket_info or not 'port' in socket_info:
        return JSONResponse(content={'status': 'error', 'message': 'No se recibió información del socket'}, status_code=500)
    
    server_ip = socket_info.get('ip')
    server_port = socket_info.get('port')
    logger.info(f'Socket received: {server_ip}:{server_port}')

    try:
        chunk_size = 50000  # Tamaño del chunk en bytes

        # Leer el archivo por chunks y enviar de uno en uno
        chunk_num = 0
        chunk = file.file.read(50000)
        writing_socket.sendto(chunk, (server_ip, server_port))
        logger.info(f'Chunk_{chunk_num} sent')


        # Wait for confirmation from the client
        confirmation, _ = listening_socket.recvfrom(1024)
        logger.info(f"Received confirmation: {confirmation.decode()}")
        time.sleep(0.2)
        chunk_num += 1
        while True:
            chunk = file.file.read(chunk_size)
            if not chunk:
                writing_socket.sendto(b'Complete', (server_ip, server_port))
                logger.info(f'=== FILE TRANSFER COMPLETED {chunk_num - 1}===')
                break
            # Send a message to the client before the next chunk
            writing_socket.sendto(b'Sending next chunk', (server_ip, server_port))
            logger.info('confirmation message sent')
            time.sleep(0.2)

            logger.info(f'Sending chunk {chunk_num}')
            writing_socket.sendto(chunk, (server_ip, server_port))  # Send the chunk to the client
            logger.info(f'Chunk sent')

            # Wait for confirmation from the client
            confirmation, _ = listening_socket.recvfrom(1024)
            logger.info(f"Received confirmation: {confirmation.decode()}")
            time.sleep(0.2)
            chunk_num += 1
    
    except Exception as e:
        logger.error(f'Error sending file chunks: {e}')
        return JSONResponse(content={'status': 'error', 'message': 'Error al enviar el archivo'}, status_code=500)

    finally:
        writing_socket.close()
        listening_socket.close()
        logger.info(f"=== CLOSING SOCKETS ===")

@app.get("/get-song-file/{title}")
def get_song_file(title):
    gateway_url = get_leader_url()
    logger.info(f'Getting song {title}')

    listening_socket, listening_port = _create_udp_socket()
    writing_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    response = requests.post(
        f'{gateway_url}/get-song-file', 
        json={
            'song_title': title, 
            'client_ip': socket.gethostbyname(socket.gethostname()), 
            'client_port': listening_port, 
            'start_chunk':0
        }
    )
    response = response.json()

    logger.info(f'response from initial request:\n{response}')

    if not 'ip' in response or not 'port' in response:
        return JSONResponse(content={'status': 'error', 'message': 'No se recibió información del socket'}, status_code=500)

    server_addr = (response['ip'], response['port'])

    def iter_chunks():
        try:
            start = 0
            chunk_num = 0
            chunk_size = 50000
            while True:
                data, addr = listening_socket.recvfrom(chunk_size)  # Buffer size of 1024 bytes
                if not data:
                    break
                logger.info(f"Received {len(data)} bytes from {addr} via UDP")
                logger.debug(f'Recieved chunk {title + str(chunk_num)} and id {get_sha_repr(title + str(chunk_num))}')
                yield data
                chunk_num += 1

                # Send a confirmation message to the server
                writing_socket.sendto(b'Data processed', server_addr)

                # Wait for the next message from the server
                server_message, _ = listening_socket.recvfrom(chunk_size)
                server_message = server_message.decode()
                logger.info(f'Received message from server: {server_message}')

                if server_message == 'Complete':
                    logger.info('Completed receiving all chunks. Closing the socket.')
                    break
                
            logger.info(f"File data for {title} received and sended to storage services")

        except Exception as e:
            logger.error(f"Error receiving file data: {e}")

        except socket.timeout:
            logger.debug(f'socket timout')
        finally:
            # Cleanup
            listening_socket.close()
            writing_socket.close()  


    return StreamingResponse(
        iter_chunks(),  # Chunks devueltos por la función
        status_code=200,  # Usamos 200 si no manejamos Range directamente
        media_type="audio/mp3",  # O el formato que uses, como audio/mp3
    )

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
        ip = socket.gethostbyname(socket.gethostname())
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((ip, 0))  # Bind to any available port
        port = udp_socket.getsockname()[1]
        logger.info(f"Listening socket created at {ip}:{port}")
        return udp_socket, port

def _receive_file_data(udp_socket, song_title: str):
        """
        Receive file data over the UDP socket and send it to storage_services.
        Args:
            udp_socket: The UDP socket object.
            file_id (str): Identifier for the file being received.
        """
        logger.info("_receive_file_data")
        def iter_chunks():
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
                        yield bytes_decoded 
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


        return StreamingResponse(
            iter_chunks(),  # Chunks devueltos por la función
            status_code=200,  # Usamos 200 si no manejamos Range directamente
            media_type="audio/mp3",  # O el formato que uses, como audio/mp3
        )
        





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)