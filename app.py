from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from pydantic import BaseModel
from typing import List
import os, time, json, requests
from fastapi import FastAPI
from discovery import discover_gateway  
import requests, logging

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
def save_song(song:dict):
    base_url = get_leader_url() 
    file = song['file']
    response = requests.post(f'{base_url}/store-song-file', json = song)
    return response.status_code

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)