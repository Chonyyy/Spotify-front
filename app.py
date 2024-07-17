from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os, re, time
import shutil

app = FastAPI()

# Configuración del middleware de CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajusta esto según tus necesidades de seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range", "Accept-Ranges", "Content-Length", "Content-Type", "X-File-Size"]
)

# Modelos de datos
class Song(BaseModel):
    id: int
    title: str
    artist: str
    genre: str
    album: str
    address: str
    img: str
    
# Datos en memoria (esto normalmente vendría de una base de datos)
songs = [
    {
        "id": 1, 
        "title": "sleep-token", 
        "artist": "agua regia",
        "genre":"rock", 
        "album":"lal", 
        "address":"music/sleep-token-aqua-regia.m4a", 
        "img":"music/sleep-token-aqua-regia_cover.jpg"
    },
    {
        "id": 1,
        "title": "What's Up",
        "artist": "4 Non Blondes",
        "genre": "pop",
        "album": "null",
        "address": "music/What's Up.mp3",
        "img": "music/What's Up_cover.jpg"
    },
    {
        "id": 1,
        "title": "In Case You Didn't Know",
        "artist": "Brett Young",
        "genre": "Country",
        "album": "Brett Young - EP",
        "address": "music/Brett Young - In Case You Didn't Know.mp3",
        "img": "music/Brett Young - In Case You Didn't Know_cover.jpg"
    },
        {
        "id": 1,
        "title": "Pedro",
        "artist": "Raffaella Carra",
        "genre": "null",
        "album": "I Miei Successi Cd01",
        "address": "music/Raffaella Carra \u2013 Pedro.mp3",
        "img": "music/Raffaella Carra \u2013 Pedro_cover.jpg"
    },
    {
        "id": 1,
        "title": "Jamie Miller - Empty Room (Official Visualizer)",
        "artist": "Jamie Miller",
        "genre": "rock",
        "album": "null",
        "address": "music/jamie-miller-empty-room.m4a",
        "img": "music/jamie-miller-empty-room_cover.jpg"
    },
]

    
@app.get("/songs", response_model=List[Song])
def get_songs(limit: int = 4, offset: int = 0):
    # Devuelve un subconjunto de canciones basado en limit y offset
    return songs[offset:offset + limit]

@app.get("/songs/{song_title}", response_model=Song)
def get_song(song_title: str):
    print(song_title)
    # Busca la canción ignorando mayúsculas y minúsculas
    song = next((song for song in songs if song["title"].lower() == song_title.lower()), None)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@app.post("/songs", response_model=Song)
def create_song(song: Song):
    songs.append(song.dict())
    return song

@app.delete("/songs/{song_id}")
def delete_song(song_id: int):
    global songs
    songs = [song for song in songs if song["id"] != song_id]
    return {"message": "Song deleted"}

@app.get("/songs/genre/{genre}", response_model=List[Song])
def get_songs_by_genre(genre: str, limit: int = 4, offset: int = 0):
    filtered_songs = [song for song in songs if song["genre"].lower() == genre.lower()]
    if not filtered_songs:
        raise HTTPException(status_code=404, detail="No songs found for the specified genre")
    return filtered_songs[offset:offset + limit]

@app.get("/songs/download/{song_id}")
def download_song(song_id: int):
    song = next((song for song in songs if song["id"] == song_id), None)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return FileResponse(song["address"], media_type='audio/mpeg', filename=song["title"])

@app.get("/songs/stream/{song_title}")
def stream_song(song_title: str, request: Request):
    # Encuentra la URL del archivo de la canción
    song_url = [s["address"] for s in songs if s["title"] == song_title]
    if not song_url:
        raise HTTPException(status_code=404, detail="Song not found")
    
    file_path = song_url[0]
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Song file not found")
    
    file_size = os.path.getsize(file_path)
    print(str(file_size))
    range_header = request.headers.get('Range')
    print(range_header)
    start = 0
    end = file_size - 1

    if range_header:
        range_match = re.match(r'bytes=(\d+)-(\d+)?', range_header)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else end

    def iterfile():
        with open(file_path, mode="rb") as file_like:
            file_like.seek(start)
            chunk_size = 1024*1024
            while chunk_size > 0:
                chunk = file_like.read(min(8192, chunk_size))
                if not chunk:
                    break
                yield chunk
                chunk_size -= len(chunk)
    
    return StreamingResponse(
        iterfile(),
        status_code=206,
        media_type="audio/mp3",
        headers={
            'Content-Range': f'bytes {start}-{end}/{file_size}',
            'Accept-Ranges': 'bytes',
            # 'Content-Length': str(end - start + 1),
            'Content-Type': 'audio/mpeg',
            'X-File-Size': str(file_size)
        }
        
    )

@app.post("/songs/upload", response_model=Song)
async def upload_song(
    file: UploadFile = File(...),
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(...),
    genre: str = Form(...),
    address: str = Form(...),
    image: UploadFile = File(None)
):
    
    
    file_location = f"music/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    img_location = ""
    if image:
        img_location = f"music/{file.filename}_cover.jpg"
        with open(img_location, "wb") as img_file:
            shutil.copyfileobj(image.file, img_file)

    new_song = {
        "id": len(songs) + 1,
        "title": title,
        "artist": artist,
        "genre": genre,
        "album": album,
        "address": file_location,
        "img": img_location
    }
    songs.append(new_song)
    return new_song

@app.post("/songs/upload_chunks", response_model=Song)
async def upload_song(
    file: UploadFile = File(...),
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(...),
    genre: str = Form(...),
    address: str = Form(...),
    image: UploadFile = File(None)
):
    chunk_size = 1024 * 1024  # 1MB chunks
    file_location = f"music/{file.filename}"
    
    with open(file_location, "wb") as f:
        while chunk := await file.read(chunk_size):
            f.write(chunk)

    img_location = ""
    if image:
        img_location = f"music/{file.filename}_cover.jpg"
        with open(img_location, "wb") as img_file:
            while chunk := await image.read(chunk_size):
                img_file.write(chunk)

    new_song = {
        "id": len(songs) + 1,
        "title": title,
        "artist": artist,
        "genre": genre,
        "album": album,
        "address": file_location,
        "img": img_location
    }
    songs.append(new_song)
    return new_song

@app.get("/songs/play/{song_id}")
def play_song(song_id: int):
    song = next((song for song in songs if song["id"] == song_id), None)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return {"address": song["address"]}

@app.get("/songs/pause")
def pause_song():
    return {"message": "Song paused"}

@app.get("/songs/resume")
def resume_song():
    return {"message": "Song resumed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)