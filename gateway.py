from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse, FileResponse
import httpx
import os
import re
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Song(BaseModel):
    id: int
    title: str
    artist: str
    genre: str
    album: str
    address: str
    img: str
  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajusta esto según tus necesidades de seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range", "Accept-Ranges", "Content-Length", "Content-Type", "X-File-Size"]
)

# Asume que estos servicios están corriendo en estas URLs
SONGS_SERVICE_URL = "http://localhost:8000"

# GET /songs
@app.get("/songs", response_model=List[Song])
async def get_songs(limit: int = 4, offset: int = 0):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SONGS_SERVICE_URL}/songs", params={"limit": limit, "offset": offset})
    return response.json()

# GET /songs/{song_title}
@app.get("/songs/{song_title}", response_model=Song)
async def get_song(song_title: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SONGS_SERVICE_URL}/songs/{song_title}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Song not found")
    return response.json()

# POST /songs
@app.post("/songs", response_model=Song)
async def create_song(song: Song):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SONGS_SERVICE_URL}/songs", json=song.dict())
    return response.json()

# DELETE /songs/{song_id}
@app.delete("/songs/{song_id}")
async def delete_song(song_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SONGS_SERVICE_URL}/songs/{song_id}")
    return response.json()

# GET /songs/genre/{genre}
@app.get("/songs/genre/{genre}", response_model=List[Song])
async def get_songs_by_genre(genre: str, limit: int = 4, offset: int = 0):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SONGS_SERVICE_URL}/songs/genre/{genre}", params={"limit": limit, "offset": offset})
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="No songs found for the specified genre")
    return response.json()

# GET /songs/download/{song_id}
@app.get("/songs/download/{song_id}")
async def download_song(song_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SONGS_SERVICE_URL}/songs/download/{song_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Song not found")
    return FileResponse(response.json()["address"], media_type='audio/mpeg', filename=response.json()["title"])

# GET /songs/stream/{song_title}
@app.get("/songs/stream/{song_title}")
async def stream_song(song_title: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SONGS_SERVICE_URL}/songs/stream/{song_title}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Song not found")
    return response

# POST /songs/upload
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
    async with httpx.AsyncClient() as client:
        files = {'file': (file.filename, file.file, file.content_type)}
        data = {'title': title, 'artist': artist, 'album': album, 'genre': genre, 'address': address}
        if image:
            files['image'] = (image.filename, image.file, image.content_type)
        response = await client.post(f"{SONGS_SERVICE_URL}/songs/upload", data=data, files=files)
    return response.json()

# POST /songs/upload_chunks
@app.post("/songs/upload_chunks", response_model=Song)
async def upload_song_chunks(
    file: UploadFile = File(...),
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(...),
    genre: str = Form(...),
    address: str = Form(...),
    image: UploadFile = File(None)
):
    async with httpx.AsyncClient() as client:
        files = {'file': (file.filename, file.file, file.content_type)}
        data = {'title': title, 'artist': artist, 'album': album, 'genre': genre, 'address': address}
        if image:
            files['image'] = (image.filename, image.file, image.content_type)
        response = await client.post(f"{SONGS_SERVICE_URL}/songs/upload_chunks", data=data, files=files)
    return response.json()

# GET /songs/play/{song_id}
@app.get("/songs/play/{song_id}")
async def play_song(song_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SONGS_SERVICE_URL}/songs/play/{song_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Song not found")
    return response.json()

# GET /songs/pause
@app.get("/songs/pause")
async def pause_song():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SONGS_SERVICE_URL}/songs/pause")
    return response.json()

# GET /songs/resume
@app.get("/songs/resume")
async def resume_song():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SONGS_SERVICE_URL}/songs/resume")
    return response.json()
