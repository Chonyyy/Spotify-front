from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os, re, json
from mutagen.mp3 import MP3

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
    
@app.get("/gw/get-songs", response_model=List[Song])
def get_songs(limit: int = 4, offset: int = 0):
    # Devuelve un subconjunto de canciones basado en limit y offset
    return songs[offset:offset + limit]

@app.post("/gw/save-song", response_model=Song)
def save_song(song: Song):
    songs.append(song.dict())
    return song

@app.get("/gw/get-songs-by-title/{song_title}", response_model=Song)
def get_songs_by_title(song_title: str):
    print(song_title)
    # Busca la canción ignorando mayúsculas y minúsculas
    song = next((song for song in songs if song["title"].lower() == song_title.lower()), None)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@app.get("/gw/get-songs-by-genre/{genre}", response_model=List[Song])
def get_songs_by_genre(genre: str, limit: int = 4, offset: int = 0):
    filtered_songs = [song for song in songs if song["genre"].lower() == genre.lower()]
    if not filtered_songs:
        raise HTTPException(status_code=404, detail="No songs found for the specified genre")
    return filtered_songs[offset:offset + limit]

@app.get("/gw/get-songs-by-artist/{artist}", response_model=List[Song]) #TODO Hacer esto en el back
def get_songs_by_artist(genre: str, limit: int = 4, offset: int = 0):
    filtered_songs = [song for song in songs if song["genre"].lower() == genre.lower()]
    if not filtered_songs:
        raise HTTPException(status_code=404, detail="No songs found for the specified genre")
    return filtered_songs[offset:offset + limit]

@app.get("/gw/store-song-file")
def store_song_file(song_title: str, request: Request):
    return "Ok"

@app.get("/songs/download/{song_id}")
def download_song(song_id: int):
    song = next((song for song in songs if song["id"] == song_id), None)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return FileResponse(song["address"], media_type='audio/mpeg', filename=song["title"])

    


# @app.get("/songs/play/{song_id}")
# def play_song(song_id: int):
#     song = next((song for song in songs if song["id"] == song_id), None)
#     if song is None:
#         raise HTTPException(status_code=404, detail="Song not found")
#     return {"address": song["address"]}

# @app.get("/songs/pause")
# def pause_song():
#     return {"message": "Song paused"}

# @app.get("/songs/resume")
# def resume_song():
#     return {"message": "Song resumed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)