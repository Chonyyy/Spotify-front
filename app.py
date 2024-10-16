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
    address: str
    img: str
    
# Datos en memoria (esto normalmente vendría de una base de datos)
# songs = [
#     {
#         "id": 1, 
#         "title": "sleep-token", 
#         "artist": "agua regia",
#         "genre":"rock", 
#         "album":"lal", 
#         "address":"music/sleep-token-aqua-regia.m4a", 
#         "img":"music/sleep-token-aqua-regia_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "What's Up",
#         "artist": "4 Non Blondes",
#         "genre": "pop",
#         "album": "null",
#         "address": "music/What's Up.mp3",
#         "img": "music/What's Up_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "In Case You Didn't Know",
#         "artist": "Brett Young",
#         "genre": "Country",
#         "album": "Brett Young - EP",
#         "address": "music/Brett Young - In Case You Didn't Know.mp3",
#         "img": "music/Brett Young - In Case You Didn't Know_cover.jpg"
#     },
#         {
#         "id": 1,
#         "title": "Pedro",
#         "artist": "Raffaella Carra",
#         "genre": "null",
#         "album": "I Miei Successi Cd01",
#         "address": "music/Raffaella Carra \u2013 Pedro.mp3",
#         "img": "music/Raffaella Carra \u2013 Pedro_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Jamie Miller - Empty Room (Official Visualizer)",
#         "artist": "Jamie Miller",
#         "genre": "rock",
#         "album": "null",
#         "address": "music/jamie-miller-empty-room.m4a",
#         "img": "music/jamie-miller-empty-room_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Demoliendo Hoteles",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Piano Bar CD 1 TRACK 1 (320).mp3",
#         "img": "music/Piano Bar CD 1 TRACK 1 (320)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Y la Felicidad Qu\u00e9",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Y la Felicidad Qu\u00e9.mp3",
#         "img": "music/Canserbero - Y la Felicidad Qu\u00e9_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hemicraneal",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/01 Estopa - Hemicraneal.mp3",
#         "img": "music/01 Estopa - Hemicraneal_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Un Misil En Mi Placard (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Soda Stereo (Remastered)",
#         "address": "music/Soda Stereo - Un Misil En Mi Placard (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Un Misil En Mi Placard (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Campos Verdes",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Campos Verdes.mp3",
#         "img": "music/Almendra - Campos Verdes_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "What's Up",
#         "artist": "4 Non Blondes",
#         "genre": "null",
#         "album": "null",
#         "address": "music/What's Up.mp3",
#         "img": "music/What's Up_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Salir De La Melancol\u00eda",
#         "artist": "Seru Giran",
#         "genre": "Rock",
#         "album": "Peperina",
#         "address": "music/10 Seru Giran - Salir De La Melancol\u00eda.mp3",
#         "img": "music/10 Seru Giran - Salir De La Melancol\u00eda_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ingravidez",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Ingravidez.mp3",
#         "img": "music/Jhamy Deja-Vu - Ingravidez_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "En todas Partes",
#         "artist": "Habana Blues",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/06 Habana Blues - En todas Partes.mp3",
#         "img": "music/06 Habana Blues - En todas Partes_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Nos Siguen Pegando Abajo",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Clics Modernos",
#         "address": "music/Charly Garc\u00eda - Nos Siguen Pegando Abajo.mp3",
#         "img": "music/Charly Garc\u00eda - Nos Siguen Pegando Abajo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Terapia De Amor Intensiva (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Doble Vida (Remastered)",
#         "address": "music/Soda Stereo - Terapia De Amor Intensiva (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Terapia De Amor Intensiva (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "47 Dogs",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - 47 Dogs.mp3",
#         "img": "music/Descartes A Kant - 47 Dogs_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Te Dejes Desanimar",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "Peliculas",
#         "address": "music/La Maquina De Hacer P\u00e1jaros - No Te Dejes Desanimar.mp3",
#         "img": "music/La Maquina De Hacer P\u00e1jaros - No Te Dejes Desanimar_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Flash",
#         "artist": "Cigarettes After Sex",
#         "genre": "Alternative",
#         "album": "Cigarettes After Sex",
#         "address": "music/05 Cigarettes After Sex - Flash.mp3",
#         "img": "music/05 Cigarettes After Sex - Flash_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Glimpse of Us",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "Glimpse of Us",
#         "address": "music/Joji - Glimpse of Us.mp3",
#         "img": "music/Joji - Glimpse of Us_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cuando Cae la Luna",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/03 Estopa - Cuando Cae la Luna.mp3",
#         "img": "music/03 Estopa - Cuando Cae la Luna_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Final",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Final.mp3",
#         "img": "music/Almendra - Final_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cuando Amanece",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/01 Estopa - Cuando Amanece.mp3",
#         "img": "music/01 Estopa - Cuando Amanece_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tele-Ka (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Soda Stereo (Remastered)",
#         "address": "music/Soda Stereo - Tele-Ka (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Tele-Ka (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vendedor De Las Chicas De Plastico",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "Peliculas",
#         "address": "music/La_Maquina_De_Hacer_P\u00e1jaros_Vendedor_De_Las_Chicas_De_Plas.mp3",
#         "img": "music/La_Maquina_De_Hacer_P\u00e1jaros_Vendedor_De_Las_Chicas_De_Plas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Se Puede Pensar Como un Prisionero",
#         "artist": "X Alfonso",
#         "genre": "Electro & Chill Out/Trip-Hop/Lounge & Rap/Hip Hop",
#         "album": "No Se Puede Pensar Como un Prisionero",
#         "address": "music/X Alfonso - No Se Puede Pensar Como un Prisionero (1).mp3",
#         "img": "music/X Alfonso - No Se Puede Pensar Como un Prisionero (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Eres Para M\u00ed",
#         "artist": "Julieta Venegas A Dueto Con Anita Tijoux",
#         "genre": "Pop",
#         "album": "Latin 101",
#         "address": "music/Julieta Venegas A Dueto Con Anita Tijoux - Eres Para M\u00ed.mp3",
#         "img": "music/Julieta Venegas A Dueto Con Anita Tijoux - Eres Para M\u00ed_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "About a Girl",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - About a Girl.mp3",
#         "img": "music/Nirvana - About a Girl_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Guernika - Dolor (UTangos - Tientos)",
#         "artist": "Diego \"El Cigala\"",
#         "genre": "null",
#         "album": "Picasso En Mis Ojos",
#         "address": "music/Diego  El Cigala  - Guernika - Dolor (UTangos - Tientos).mp3",
#         "img": "music/Diego  El Cigala  - Guernika - Dolor (UTangos - Tientos)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Jamie Miller - Empty Room (Official Visualizer)",
#         "artist": "Jamie Miller",
#         "genre": "null",
#         "album": "null",
#         "address": "music/jamie-miller-empty-room.m4a",
#         "img": "music/jamie-miller-empty-room_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Momma",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - Momma.mp3",
#         "img": "music/Kendrick Lamar - Momma_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Voodoo?",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Voodoo.mp3",
#         "img": "music/L Imp\u00e9ratrice - Voodoo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Interludio K219",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Interludio K219.mp3",
#         "img": "music/Canserbero - Interludio K219_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Bailando en la Distancia",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Real World",
#         "address": "music/X Alfonso - Bailando en la Distancia.mp3",
#         "img": "music/X Alfonso - Bailando en la Distancia_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tragicomedia",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Tragicomedia.mp3",
#         "img": "music/Estopa - Tragicomedia_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Y deja (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Y deja (Remastered).mp3",
#         "img": "music/Los Zafiros - Y deja (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Y sabes bien (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Y sabes bien (Remastered).mp3",
#         "img": "music/Los Zafiros - Y sabes bien (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Rumba Ke Tumba",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/04 Estopa - Rumba Ke Tumba.mp3",
#         "img": "music/04 Estopa - Rumba Ke Tumba_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Revuelto",
#         "artist": "Cimafunk",
#         "genre": "null",
#         "album": "Terapia",
#         "address": "music/Cimafunk - Revuelto.mp3",
#         "img": "music/Cimafunk - Revuelto_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "A Mi Me Gusta",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/06 Estopa - A Mi Me Gusta.mp3",
#         "img": "music/06 Estopa - A Mi Me Gusta_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cuando Pase El Temblor (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Ruido Blanco (Remastered)",
#         "address": "music/Soda Stereo - Cuando Pase El Temblor (Remasterizado 2007) (1).mp3",
#         "img": "music/Soda Stereo - Cuando Pase El Temblor (Remasterizado 2007) (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Sed Verdadera",
#         "artist": "Pescado Rabioso",
#         "genre": "Rock",
#         "album": "Artaud",
#         "address": "music/Pescado Rabioso - La Sed Verdadera.mp3",
#         "img": "music/Pescado Rabioso - La Sed Verdadera_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "gn / intro",
#         "artist": "Nour",
#         "genre": "null",
#         "album": "daydreamer",
#         "address": "music/Nour - gn _ intro.mp3",
#         "img": "music/Nour - gn _ intro_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Esperando Nacer",
#         "artist": "Seru Giran",
#         "genre": "Rock",
#         "album": "Peperina",
#         "address": "music/05 Seru Giran - Esperando Nacer.mp3",
#         "img": "music/05 Seru Giran - Esperando Nacer_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ojos De Video Tape",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Clics Modernos",
#         "address": "music/Charly Garc\u00eda - Ojos De Video Tape.mp3",
#         "img": "music/Charly Garc\u00eda - Ojos De Video Tape_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cuerpo Triste",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/02 Estopa - Cuerpo Triste.mp3",
#         "img": "music/02 Estopa - Cuerpo Triste_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Opera House",
#         "artist": "Cigarettes After Sex",
#         "genre": "Vaihtoehtoinen",
#         "album": "Cigarettes After Sex",
#         "address": "music/07 Cigarettes After Sex - Opera House.mp3",
#         "img": "music/07 Cigarettes After Sex - Opera House_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ley del Hielo",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Ley del Hielo.mp3",
#         "img": "music/Canserbero - Ley del Hielo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "S\u00e9 Feliz",
#         "artist": "Anais Abreu",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/16 Anais Abreu - S\u00e9 Feliz.mp3",
#         "img": "music/16 Anais Abreu - S\u00e9 Feliz_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mi Primera Cana",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Mi Primera Cana.mp3",
#         "img": "music/Estopa - Mi Primera Cana_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Arenas de Soledad",
#         "artist": "Habana Blues",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/05 Habana Blues - Arenas de Soledad.mp3",
#         "img": "music/05 Habana Blues - Arenas de Soledad_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "En La Cama O En El Suelo (Remastered)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los_Abuelos_de_la_Nada_En_La_Cama_O_En_El_Suelo_Remastered.mp3",
#         "img": "music/Los_Abuelos_de_la_Nada_En_La_Cama_O_En_El_Suelo_Remastered_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Basta Que Lo Digas T\u00fa",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Basta Que Lo Digas T\u00fa.mp3",
#         "img": "music/Habana Abierta - Basta Que Lo Digas T\u00fa_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cancion Para Mi Muerte (Bonus Track)",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Charly Garc\u00eda - Cancion Para Mi Muerte (Bonus Track).mp3",
#         "img": "music/Charly Garc\u00eda - Cancion Para Mi Muerte (Bonus Track)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Astronaut",
#         "artist": "Uma",
#         "genre": "null",
#         "album": "Bel\u2022li",
#         "address": "music/Uma - Astronaut.mp3",
#         "img": "music/Uma - Astronaut_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mundo de Piedra",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - Mundo de Piedra.mp3",
#         "img": "music/Canserbero - Mundo de Piedra_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Que Va a Ser de Ti",
#         "artist": "Joan Manuel Serrat",
#         "genre": "Pop & International Pop & Latin Music",
#         "album": "Mediterr\u00e1neo",
#         "address": "music/Joan Manuel Serrat - Que Va a Ser de Ti.mp3",
#         "img": "music/Joan Manuel Serrat - Que Va a Ser de Ti_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hermosa Habana",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Locura Azul - Original Soundtrack CD 1 TRACK 1 (320).mp3",
#         "img": "music/Locura Azul - Original Soundtrack CD 1 TRACK 1 (320)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mas de Ti",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Mas de Ti.mp3",
#         "img": "music/Jhamy Deja-Vu - Mas de Ti_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Apenao - Toro (Rumba)",
#         "artist": "Diego \"El Cigala\"",
#         "genre": "null",
#         "album": "Picasso En Mis Ojos",
#         "address": "music/Diego  El Cigala  - Apenao - Toro (Rumba).mp3",
#         "img": "music/Diego  El Cigala  - Apenao - Toro (Rumba)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Raindrops Of Poison",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - Raindrops Of Poison.mp3",
#         "img": "music/Descartes A Kant - Raindrops Of Poison_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "R.I.P. (feat. Trippie Redd)",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - R.I.P. (feat. Trippie Redd).mp3",
#         "img": "music/Joji - R.I.P. (feat. Trippie Redd)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "You Ain't Gotta Lie (Momma Said)",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - You Ain't Gotta Lie (Momma Said).mp3",
#         "img": "music/Kendrick Lamar - You Ain't Gotta Lie (Momma Said)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "u",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - u.mp3",
#         "img": "music/Kendrick Lamar - u_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Bossa Cubana",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Locura Azul - Original Soundtrack CD 1 TRACK 9 (320).mp3",
#         "img": "music/Locura Azul - Original Soundtrack CD 1 TRACK 9 (320)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Gato y el Rat\u00f3n",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - El Gato y el Rat\u00f3n.mp3",
#         "img": "music/Habana Abierta - El Gato y el Rat\u00f3n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Te Enamores Nunca De Aquel Marinero Bengal\u00ed (Mix Dance 1995)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada",
#         "address": "music/Los_Abuelos_de_la_Nada_No_Te_Enamores_Nunca_De_Aquel_Marinero_Bengal\u00ed.mp3",
#         "img": "music/Los_Abuelos_de_la_Nada_No_Te_Enamores_Nunca_De_Aquel_Marinero_Bengal\u00ed_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Matraca",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/05 Estopa - La Matraca.mp3",
#         "img": "music/05 Estopa - La Matraca_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "bahr",
#         "artist": "Nour",
#         "genre": "null",
#         "album": "daydreamer",
#         "address": "music/Nour - bahr.mp3",
#         "img": "music/Nour - bahr_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Mundo Entre Las Manos",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - El Mundo Entre Las Manos.mp3",
#         "img": "music/Almendra - El Mundo Entre Las Manos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Final Caja Negra (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Ruido Blanco (Remastered)",
#         "address": "music/Soda Stereo - Final Caja Negra (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Final Caja Negra (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Restart And Heal",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - Restart And Heal.mp3",
#         "img": "music/Descartes A Kant - Restart And Heal_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Paciente",
#         "artist": "Cimafunk",
#         "genre": "null",
#         "album": "Terapia",
#         "address": "music/Cimafunk - Paciente.mp3",
#         "img": "music/Cimafunk - Paciente_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cantata de Puentes Amarillos",
#         "artist": "Pescado Rabioso",
#         "genre": "Rock",
#         "album": "Artaud",
#         "address": "music/Pescado Rabioso - Cantata de Puentes Amarillos.mp3",
#         "img": "music/Pescado Rabioso - Cantata de Puentes Amarillos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tr\u00e1tame Suavemente (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Tr\u00e1tame Suavemente (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Tr\u00e1tame Suavemente (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pedro",
#         "artist": "Raffaella Carra",
#         "genre": "null",
#         "album": "I Miei Successi Cd01",
#         "address": "music/Raffaella Carra \u2013 Pedro.mp3",
#         "img": "music/Raffaella Carra \u2013 Pedro_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ni Un Segundo (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Soda Stereo (Remastered)",
#         "address": "music/Soda Stereo - Ni Un Segundo (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Ni Un Segundo (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Janine (2015 Remaster)",
#         "artist": "David Bowie",
#         "genre": "Pop",
#         "album": "David Bowie (aka Space Oddity) (2015 Remaster)",
#         "address": "music/David Bowie - Janine (2015 Remaster).mp3",
#         "img": "music/David Bowie - Janine (2015 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pastillas de Freno",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/09 Estopa - Pastillas de Freno.mp3",
#         "img": "music/09 Estopa - Pastillas de Freno_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Relajito",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - El Relajito.mp3",
#         "img": "music/Habana Abierta - El Relajito_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Dive (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Dive (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - Dive (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "J'aime \u00e0 nouveau",
#         "artist": "ZAZ",
#         "genre": "Pop",
#         "album": "Zaz",
#         "address": "music/09 ZAZ - J aime \u00e0 nouveau.mp3",
#         "img": "music/09 ZAZ - J aime \u00e0 nouveau_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Coraz\u00f3n Boomerang",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Coraz\u00f3n Boomerang.mp3",
#         "img": "music/Habana Abierta - Coraz\u00f3n Boomerang_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Digital Sunset",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Digital Sunset.mp3",
#         "img": "music/L Imp\u00e9ratrice - Digital Sunset_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "\u00a1Ah!...Basta de Pensar",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "null",
#         "album": "Kamikaze",
#         "address": "music/Luis Alberto Spinetta -  Ah!...Basta de Pensar.mp3",
#         "img": "music/Luis Alberto Spinetta -  Ah!...Basta de Pensar_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vous",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/05 Camille - Vous.mp3",
#         "img": "music/05 Camille - Vous_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Dans ma rue",
#         "artist": "ZAZ",
#         "genre": "Pop",
#         "album": "Zaz",
#         "address": "music/10 ZAZ - Dans ma rue.mp3",
#         "img": "music/10 ZAZ - Dans ma rue_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Chocolate Con Churro",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Chocolate Con Churro.mp3",
#         "img": "music/Habana Abierta - Chocolate Con Churro_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "As\u00ed Es El Calor (Remastered)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los Abuelos de la Nada - As\u00ed Es El Calor (Remastered).mp3",
#         "img": "music/Los Abuelos de la Nada - As\u00ed Es El Calor (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Dazed and Confused (2014 Remaster)",
#         "artist": "Led Zeppelin",
#         "genre": "Rock",
#         "album": "Led Zeppelin",
#         "address": "music/Led Zeppelin - Dazed and Confused (2014 Remaster).mp3",
#         "img": "music/Led Zeppelin - Dazed and Confused (2014 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Au port",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/11 Camille - Au port.mp3",
#         "img": "music/11 Camille - Au port_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Letter to Hermione (2015 Remaster)",
#         "artist": "David Bowie",
#         "genre": "Pop",
#         "album": "David Bowie (aka Space Oddity) (2015 Remaster)",
#         "address": "music/David Bowie - Letter to Hermione (2015 Remaster).mp3",
#         "img": "music/David Bowie - Letter to Hermione (2015 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Lumi\u00e8re",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/18 Camille - Lumi\u00e8re.mp3",
#         "img": "music/18 Camille - Lumi\u00e8re_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ah Te Vi Entre Las Luces",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "Pop",
#         "album": "La M\u00e1quina De Hacer P\u00e1jaros",
#         "address": "music/07 La Maquina De Hacer P\u00e1jaros - Ah Te Vi Entre Las Luces.mp3",
#         "img": "music/07 La Maquina De Hacer P\u00e1jaros - Ah Te Vi Entre Las Luces_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Descatalogando",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/10 Estopa - Descatalogando.mp3",
#         "img": "music/10 Estopa - Descatalogando_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hipercandombe",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "Peliculas",
#         "address": "music/La Maquina De Hacer P\u00e1jaros - Hipercandombe.mp3",
#         "img": "music/La Maquina De Hacer P\u00e1jaros - Hipercandombe_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "A Catastrophe",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - A Catastrophe.mp3",
#         "img": "music/Descartes A Kant - A Catastrophe_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "C'est La Mort",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - C'est La Mort.mp3",
#         "img": "music/Canserbero - C'est La Mort_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Son Iguales",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Son Iguales.mp3",
#         "img": "music/Habana Abierta - Son Iguales_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Qui\u00e9reme vidita (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Qui\u00e9reme vidita (Remastered).mp3",
#         "img": "music/Los Zafiros - Qui\u00e9reme vidita (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "outta control",
#         "artist": "Nour",
#         "genre": "null",
#         "album": "daydreamer",
#         "address": "music/Nour - outta control.mp3",
#         "img": "music/Nour - outta control_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cuando Amanece",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/02 Estopa - Cuando Amanece.mp3",
#         "img": "music/02 Estopa - Cuando Amanece_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Otra Vez una Se\u00f1al",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Reverse",
#         "address": "music/X Alfonso - Otra Vez una Se\u00f1al.mp3",
#         "img": "music/X Alfonso - Otra Vez una Se\u00f1al_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Eres Tu",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Real World",
#         "address": "music/X Alfonso - No Eres Tu.mp3",
#         "img": "music/X Alfonso - No Eres Tu_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Molly's Lips (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Molly's Lips (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - Molly's Lips (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ponte Pa' Lo Tuyo",
#         "artist": "Cimafunk",
#         "genre": "null",
#         "album": "Terapia",
#         "address": "music/Cimafunk - Ponte Pa  Lo Tuyo.mp3",
#         "img": "music/Cimafunk - Ponte Pa  Lo Tuyo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Era Est\u00e1 Pariendo un Coraz\u00f3n",
#         "artist": "Silvio Rodr\u00edguez",
#         "genre": "Singer & Songwriter",
#         "album": "Al Final de Este Viaje...",
#         "address": "music/Silvio Rodr\u00edguez - La Era Est\u00e1 Pariendo un Coraz\u00f3n.mp3",
#         "img": "music/Silvio Rodr\u00edguez - La Era Est\u00e1 Pariendo un Coraz\u00f3n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Veinte Trajes Verdes",
#         "artist": "Seru Giran",
#         "genre": "Rock",
#         "album": "Peperina",
#         "address": "music/06 Seru Giran - Veinte Trajes Verdes.mp3",
#         "img": "music/06 Seru Giran - Veinte Trajes Verdes_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sin Mercy",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - Sin Mercy.mp3",
#         "img": "music/Canserbero - Sin Mercy_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mr. Moustache",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Mr. Moustache.mp3",
#         "img": "music/Nirvana - Mr. Moustache_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Fiebre",
#         "artist": "Cimafunk",
#         "genre": "null",
#         "album": "Terapia",
#         "address": "music/Cimafunk - Fiebre.mp3",
#         "img": "music/Cimafunk - Fiebre_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Llorando En El Espejo",
#         "artist": "Seru Giran",
#         "genre": "Rock",
#         "album": "Peperina",
#         "address": "music/02 Seru Giran - Llorando En El Espejo.mp3",
#         "img": "music/02 Seru Giran - Llorando En El Espejo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Four Sticks (2012 Remaster)",
#         "artist": "Led Zeppelin",
#         "genre": "Rock",
#         "album": "Led Zeppelin IV (Deluxe Edition; Remaster)",
#         "address": "music/Led Zeppelin - Four Sticks (2012 Remaster).mp3",
#         "img": "music/Led Zeppelin - Four Sticks (2012 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "the WORLD (TV Size)",
#         "artist": "Nightmare",
#         "genre": "null",
#         "album": "DEATH NOTE Original Soundtrack",
#         "address": "music/Nightmare - the WORLD (TV Size).mp3",
#         "img": "music/Nightmare - the WORLD (TV Size)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Aquellas Peque\u00f1as Cosas",
#         "artist": "Joan Manuel Serrat",
#         "genre": "Pop & Rock",
#         "album": "24 Paginas Inolvidables",
#         "address": "music/Joan Manuel Serrat - Aquellas Peque\u00f1as Cosas.mp3",
#         "img": "music/Joan Manuel Serrat - Aquellas Peque\u00f1as Cosas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Marilyn, La Cenicienta Y Las Mujeres",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "Peliculas",
#         "address": "music/La_Maquina_De_Hacer_P\u00e1jaros_Marilyn,_La_Cenicienta_Y_Las_M.mp3",
#         "img": "music/La_Maquina_De_Hacer_P\u00e1jaros_Marilyn,_La_Cenicienta_Y_Las_M_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Superfinos negros",
#         "artist": "Free Hole Negro",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/10 Free Hole Negro - Superfinos negros.mp3",
#         "img": "music/10 Free Hole Negro - Superfinos negros_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ojal\u00e1",
#         "artist": "Silvio Rodr\u00edguez",
#         "genre": "Singer & Songwriter",
#         "album": "Al Final de Este Viaje...",
#         "address": "music/Silvio Rodr\u00edguez - Ojal\u00e1.mp3",
#         "img": "music/Silvio Rodr\u00edguez - Ojal\u00e1_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "C\u00f3mo Debo Andar (Remastered)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los Abuelos de la Nada - C\u00f3mo Debo Andar (Remastered).mp3",
#         "img": "music/Los Abuelos de la Nada - C\u00f3mo Debo Andar (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mi oraci\u00f3n (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Mi oraci\u00f3n (Remastered).mp3",
#         "img": "music/Los Zafiros - Mi oraci\u00f3n (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "F\u00e1bricas de Sue\u00f1os",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/11 Estopa - F\u00e1bricas de Sue\u00f1os.mp3",
#         "img": "music/11 Estopa - F\u00e1bricas de Sue\u00f1os_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Dime",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Reverse",
#         "address": "music/X Alfonso - Dime.mp3",
#         "img": "music/X Alfonso - Dime_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Parado En El Medio De La Vida",
#         "artist": "Seru Giran",
#         "genre": "Rock",
#         "album": "Peperina",
#         "address": "music/03 Seru Giran - Parado En El Medio De La Vida.mp3",
#         "img": "music/03 Seru Giran - Parado En El Medio De La Vida_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Peur des filles",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Peur des filles.mp3",
#         "img": "music/L Imp\u00e9ratrice - Peur des filles_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Plateado Sobre Plateado (Huellas En El Mar)",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Clics Modernos",
#         "address": "music/Charly Garc\u00eda - Plateado Sobre Plateado (Huellas En El Mar).mp3",
#         "img": "music/Charly Garc\u00eda - Plateado Sobre Plateado (Huellas En El Mar)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Persiana Americana (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Ruido Blanco (Remastered)",
#         "address": "music/Soda Stereo - Persiana Americana (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Persiana Americana (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Beautiful",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Beautiful.mp3",
#         "img": "music/Jhamy Deja-Vu - Beautiful_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Una Broma Seria",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Una Broma Seria.mp3",
#         "img": "music/Habana Abierta - Una Broma Seria_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "K.",
#         "artist": "Cigarettes After Sex",
#         "genre": "Alternative",
#         "album": "Cigarettes After Sex",
#         "address": "music/01 Cigarettes After Sex - K..mp3",
#         "img": "music/01 Cigarettes After Sex - K._cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mi Novia Tiene B\u00edceps (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Soda Stereo (Remastered)",
#         "address": "music/Soda Stereo - Mi Novia Tiene B\u00edceps (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Mi Novia Tiene B\u00edceps (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Laura Va",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Laura Va.mp3",
#         "img": "music/Almendra - Laura Va_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Senza",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/08 Camille - Senza.mp3",
#         "img": "music/08 Camille - Senza_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Gulere Gulere",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/07 Estopa - Gulere Gulere.mp3",
#         "img": "music/07 Estopa - Gulere Gulere_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "En el Valle de las Sombras",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - En el Valle de las Sombras.mp3",
#         "img": "music/Canserbero - En el Valle de las Sombras_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Coraz\u00f3n Aerodin\u00e1mico",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Coraz\u00f3n Aerodin\u00e1mico.mp3",
#         "img": "music/Estopa - Coraz\u00f3n Aerodin\u00e1mico_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Floyd the Barber",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Floyd the Barber.mp3",
#         "img": "music/Nirvana - Floyd the Barber_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sobredosis de T.V. (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Sobredosis de T.V. (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Sobredosis de T.V. (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Puchunguita ven (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Puchunguita ven (Remastered).mp3",
#         "img": "music/Los Zafiros - Puchunguita ven (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vacaciones",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/03 Estopa - Vacaciones.mp3",
#         "img": "music/03 Estopa - Vacaciones_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "De Mi Muerte",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - De Mi Muerte.mp3",
#         "img": "music/Canserbero - De Mi Muerte_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Port Coton",
#         "artist": "ZAZ",
#         "genre": "Pop",
#         "album": "Zaz",
#         "address": "music/08 ZAZ - Port Coton.mp3",
#         "img": "music/08 ZAZ - Port Coton_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pour que l'amour me quitte",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/07 Camille - Pour que l'amour me quitte.mp3",
#         "img": "music/07 Camille - Pour que l'amour me quitte_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Swap Meet",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Swap Meet.mp3",
#         "img": "music/Nirvana - Swap Meet_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tuve Tu Amor",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Charly Garc\u00eda - Tuve Tu Amor.mp3",
#         "img": "music/Charly Garc\u00eda - Tuve Tu Amor_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La jeune fille aux cheveux blancs",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/01 Camille - La jeune fille aux cheveux blancs.mp3",
#         "img": "music/01 Camille - La jeune fille aux cheveux blancs_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sara el Amor",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Los Zafiros - Sara el Amor.mp3",
#         "img": "music/Los Zafiros - Sara el Amor_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cuando Cae la Luna",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Cuando Cae la Luna.mp3",
#         "img": "music/Estopa - Cuando Cae la Luna_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Chanelando - Pintor (Tangos)",
#         "artist": "Diego \"El Cigala\"",
#         "genre": "null",
#         "album": "Picasso En Mis Ojos",
#         "address": "music/Diego  El Cigala  - Chanelando - Pintor (Tangos).mp3",
#         "img": "music/Diego  El Cigala  - Chanelando - Pintor (Tangos)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Observ\u00e1ndonos (Sat\u00e9lites) (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Nada Personal (Remastered)",
#         "address": "music/Soda_Stereo_Observ\u00e1ndonos_Sat\u00e9lites_Remasterizado_2007.mp3",
#         "img": "music/Soda_Stereo_Observ\u00e1ndonos_Sat\u00e9lites_Remasterizado_2007_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "He venido a decirte (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - He venido a decirte (Remastered).mp3",
#         "img": "music/Los Zafiros - He venido a decirte (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hermana Teresa (Remastered)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los Abuelos de la Nada - Hermana Teresa (Remastered).mp3",
#         "img": "music/Los Abuelos de la Nada - Hermana Teresa (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Al Final de Este Viaje en la Vida",
#         "artist": "Silvio Rodr\u00edguez",
#         "genre": "Singer & Songwriter",
#         "album": "Al Final de Este Viaje...",
#         "address": "music/Silvio Rodr\u00edguez - Al Final de Este Viaje en la Vida.mp3",
#         "img": "music/Silvio Rodr\u00edguez - Al Final de Este Viaje en la Vida_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Love Buzz",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Love Buzz.mp3",
#         "img": "music/Nirvana - Love Buzz_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Falsa",
#         "artist": "Toques del R\u00edo",
#         "genre": "Lateinamerikanische Musik",
#         "album": "P\u00e1 Que Te Sosiegues",
#         "address": "music/09 Toques del R\u00edo - Falsa.mp3",
#         "img": "music/09 Toques del R\u00edo - Falsa_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Luna de Plata - Gitana (Buleria)",
#         "artist": "Diego \"El Cigala\"",
#         "genre": "null",
#         "album": "Picasso En Mis Ojos",
#         "address": "music/Diego  El Cigala  - Luna de Plata - Gitana (Buleria).mp3",
#         "img": "music/Diego  El Cigala  - Luna de Plata - Gitana (Buleria)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Mujer Que Yo Quiero",
#         "artist": "Joan Manuel Serrat",
#         "genre": "Pop & Rock",
#         "album": "24 Paginas Inolvidables",
#         "address": "music/Joan Manuel Serrat - La Mujer Que Yo Quiero.mp3",
#         "img": "music/Joan Manuel Serrat - La Mujer Que Yo Quiero_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Aciertos",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Aciertos.mp3",
#         "img": "music/Jhamy Deja-Vu - Aciertos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Aqua Regia",
#         "artist": "Sleep Token",
#         "genre": "null",
#         "album": "Take Me Back To Eden",
#         "address": "music/sleep-token-aqua-regia.m4a",
#         "img": "music/sleep-token-aqua-regia_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ya No Me Acuerdo",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/05 Estopa - Ya No Me Acuerdo.mp3",
#         "img": "music/05 Estopa - Ya No Me Acuerdo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Assise",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/03 Camille - Assise.mp3",
#         "img": "music/03 Camille - Assise_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Been a Son (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Been a Son (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - Been a Son (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Plegaria Para Un Ni\u00f1o Dormido",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Plegaria Para Un Ni\u00f1o Dormido.mp3",
#         "img": "music/Almendra - Plegaria Para Un Ni\u00f1o Dormido_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "A Estos Hombres Tristes",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - A Estos Hombres Tristes.mp3",
#         "img": "music/Almendra - A Estos Hombres Tristes_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La rue de M\u00e9nilmontant",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/14 Camille - La rue de M\u00e9nilmontant.mp3",
#         "img": "music/14 Camille - La rue de M\u00e9nilmontant_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Complexion (A Zulu Love)",
#         "artist": "Kendrick Lamar, Rapsody",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar, Rapsody - Complexion (A Zulu Love).mp3",
#         "img": "music/Kendrick Lamar, Rapsody - Complexion (A Zulu Love)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cacho a Cacho",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/06 Estopa - Cacho a Cacho.mp3",
#         "img": "music/06 Estopa - Cacho a Cacho_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Hora del Juicio",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - La Hora del Juicio.mp3",
#         "img": "music/Canserbero - La Hora del Juicio_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "The Blacker The Berry",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - The Blacker The Berry.mp3",
#         "img": "music/Kendrick Lamar - The Blacker The Berry_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Luna Lunera",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Luna Lunera.mp3",
#         "img": "music/Estopa - Luna Lunera_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Juegos De Seducci\u00f3n (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Alternative & Indie Pop & Indie Rock & Pop & Indie Pop/Folk & Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Juegos De Seducci\u00f3n (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Juegos De Seducci\u00f3n (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "I'LL SEE YOU IN 40",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - I LL SEE YOU IN 40.mp3",
#         "img": "music/Joji - I LL SEE YOU IN 40_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Me Digas Adi\u00f3s",
#         "artist": "Toques del R\u00edo",
#         "genre": "Latinalainen musiikki",
#         "album": "P\u00e1 Que Te Sosiegues",
#         "address": "music/04 Toques del R\u00edo - No Me Digas Adi\u00f3s.mp3",
#         "img": "music/04 Toques del R\u00edo - No Me Digas Adi\u00f3s_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ana No Duerme",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Ana No Duerme.mp3",
#         "img": "music/Almendra - Ana No Duerme_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Bubulina",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "La M\u00e1quina De Hacer P\u00e1jaros",
#         "address": "music/La Maquina De Hacer P\u00e1jaros - Bubulina.mp3",
#         "img": "music/La Maquina De Hacer P\u00e1jaros - Bubulina_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "P\u00e2le Septembre",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/13 Camille - P\u00e2le Septembre.mp3",
#         "img": "music/13 Camille - P\u00e2le Septembre_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Run Run",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/01 Estopa - El Run Run.mp3",
#         "img": "music/01 Estopa - El Run Run_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Curandera",
#         "artist": "Kelvis Ochoa",
#         "genre": "None",
#         "album": "Curanderas",
#         "address": "music/05 Kelvis Ochoa - Curandera.mp3",
#         "img": "music/05 Kelvis Ochoa - Curandera_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "When the Levee Breaks (2012 Remaster)",
#         "artist": "Led Zeppelin",
#         "genre": "Rock",
#         "album": "Led Zeppelin IV (Deluxe Edition; Remaster)",
#         "address": "music/Led Zeppelin - When the Levee Breaks (2012 Remaster).mp3",
#         "img": "music/Led Zeppelin - When the Levee Breaks (2012 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "\u00c1guila de Trueno (Parte II)",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "null",
#         "album": "Kamikaze",
#         "address": "music/Luis Alberto Spinetta - \u00c1guila de Trueno (Parte II).mp3",
#         "img": "music/Luis Alberto Spinetta - \u00c1guila de Trueno (Parte II)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sazona`o",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Sazona`o.mp3",
#         "img": "music/Jhamy Deja-Vu - Sazona`o_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Blade",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - El Blade.mp3",
#         "img": "music/Estopa - El Blade_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "En L\u00ednea (Remastered)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los Abuelos de la Nada - En L\u00ednea (Remastered).mp3",
#         "img": "music/Los Abuelos de la Nada - En L\u00ednea (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Signos (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Ruido Blanco (Remastered)",
#         "address": "music/Soda Stereo - Signos (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Signos (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Que El Viento Borr\u00f3 Tus Manos",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Que El Viento Borr\u00f3 Tus Manos.mp3",
#         "img": "music/Almendra - Que El Viento Borr\u00f3 Tus Manos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Por",
#         "artist": "Pescado Rabioso",
#         "genre": "Rock",
#         "album": "Artaud",
#         "address": "music/Pescado Rabioso - Por.mp3",
#         "img": "music/Pescado Rabioso - Por_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Perdiendo la Fe",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Perdiendo la Fe.mp3",
#         "img": "music/Canserbero - Perdiendo la Fe_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Overture",
#         "artist": "Uma",
#         "genre": "null",
#         "album": "Bel\u2022li",
#         "address": "music/Uma - Overture.mp3",
#         "img": "music/Uma - Overture_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Debo Partirme en Dos",
#         "artist": "Silvio Rodr\u00edguez",
#         "genre": "Singer & Songwriter",
#         "album": "Al Final de Este Viaje...",
#         "address": "music/Silvio Rodr\u00edguez - Debo Partirme en Dos.mp3",
#         "img": "music/Silvio Rodr\u00edguez - Debo Partirme en Dos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Le long de la route",
#         "artist": "ZAZ",
#         "genre": "Pop",
#         "album": "Zaz",
#         "address": "music/03 ZAZ - Le long de la route.mp3",
#         "img": "music/03 ZAZ - Le long de la route_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Parar el Tiempo",
#         "artist": "Cimafunk",
#         "genre": "null",
#         "album": "Terapia",
#         "address": "music/Cimafunk - Parar el Tiempo.mp3",
#         "img": "music/Cimafunk - Parar el Tiempo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Bancate Ese Defecto",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Clics Modernos",
#         "address": "music/Charly Garc\u00eda - Bancate Ese Defecto.mp3",
#         "img": "music/Charly Garc\u00eda - Bancate Ese Defecto_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Si No Fuera Por... (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Nada Personal (Remastered)",
#         "address": "music/Soda Stereo - Si No Fuera Por... (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Si No Fuera Por... (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Almendra",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "Rock",
#         "album": "Kamikaze",
#         "address": "music/05 Luis Alberto Spinetta - Almendra.mp3",
#         "img": "music/05 Luis Alberto Spinetta - Almendra_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Si Tu Te Vas",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Real World",
#         "address": "music/X Alfonso - Si Tu Te Vas.mp3",
#         "img": "music/X Alfonso - Si Tu Te Vas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Hay Azul Sin Ti",
#         "artist": "X Alfonso",
#         "genre": "Alternative & Reggae",
#         "album": "No Hay Azul Sin Ti",
#         "address": "music/X Alfonso - No Hay Azul Sin Ti (1).mp3",
#         "img": "music/X Alfonso - No Hay Azul Sin Ti (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Y sigo (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Y sigo (Remastered).mp3",
#         "img": "music/Los Zafiros - Y sigo (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Son Palabras, Son Mis Huellas",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "No Son Palabras, Son Mis Huellas",
#         "address": "music/X Alfonso - No Son Palabras, Son Mis Huellas (1).mp3",
#         "img": "music/X Alfonso - No Son Palabras, Son Mis Huellas (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mortal Man",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - Mortal Man.mp3",
#         "img": "music/Kendrick Lamar - Mortal Man_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Aventura de la Abeja Reina",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "null",
#         "album": "Kamikaze",
#         "address": "music/Luis Alberto Spinetta - La Aventura de la Abeja Reina.mp3",
#         "img": "music/Luis Alberto Spinetta - La Aventura de la Abeja Reina_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ep\u00edlogo",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Ep\u00edlogo.mp3",
#         "img": "music/Canserbero - Ep\u00edlogo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Lo Que Dice La Lluvia",
#         "artist": "Seru Giran",
#         "genre": "Rock",
#         "album": "Peperina",
#         "address": "music/11 Seru Giran - Lo Que Dice La Lluvia.mp3",
#         "img": "music/11 Seru Giran - Lo Que Dice La Lluvia_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tu Calorro",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/04 Estopa - Tu Calorro.mp3",
#         "img": "music/04 Estopa - Tu Calorro_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mayonaka no Door / Stay With Me",
#         "artist": "Miki Matsubara",
#         "genre": "Asiatische Musik",
#         "album": "Miki Matsubara Best Collection",
#         "address": "music/04 Miki Matsubara - Mayonaka no Door _ Stay With Me.mp3",
#         "img": "music/04 Miki Matsubara - Mayonaka no Door _ Stay With Me_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Silver Tongue",
#         "artist": "Uma",
#         "genre": "null",
#         "album": "Bel\u2022li",
#         "address": "music/Uma - Silver Tongue.mp3",
#         "img": "music/Uma - Silver Tongue_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "departure!",
#         "artist": "Masatoshi Ono",
#         "genre": "null",
#         "album": "departure!",
#         "address": "music/Masatoshi Ono - departure!.mp3",
#         "img": "music/Masatoshi Ono - departure!_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Malabares",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/01 Estopa - Malabares.mp3",
#         "img": "music/01 Estopa - Malabares_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Las Habladurias del Mundo",
#         "artist": "Pescado Rabioso",
#         "genre": "Rock",
#         "album": "Artaud",
#         "address": "music/Pescado Rabioso - Las Habladurias del Mundo.mp3",
#         "img": "music/Pescado Rabioso - Las Habladurias del Mundo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "D\u00eda Com\u00fan- Doble Vida (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Doble Vida (Remastered)",
#         "address": "music/Soda Stereo - D\u00eda Com\u00fan- Doble Vida (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - D\u00eda Com\u00fan- Doble Vida (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Coraz\u00f3n Delator (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Coraz\u00f3n Delator (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Coraz\u00f3n Delator (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Dime Qu\u00e9 Hay Que Hacer",
#         "artist": "X Alfonso",
#         "genre": "Rap/Hip Hop",
#         "album": "Dime Qu\u00e9 Hay Que Hacer",
#         "address": "music/X Alfonso - Dime Qu\u00e9 Hay Que Hacer (1).mp3",
#         "img": "music/X Alfonso - Dime Qu\u00e9 Hay Que Hacer (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Boca Abajo",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Boca Abajo.mp3",
#         "img": "music/Habana Abierta - Boca Abajo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Qued\u00e1ndote o Y\u00e9ndote",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "Rock",
#         "album": "Kamikaze",
#         "address": "music/10 Luis Alberto Spinetta - Qued\u00e1ndote o Y\u00e9ndote.mp3",
#         "img": "music/10 Luis Alberto Spinetta - Qued\u00e1ndote o Y\u00e9ndote_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Perfecto Balance",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Perfecto Balance.mp3",
#         "img": "music/Jhamy Deja-Vu - Perfecto Balance_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Algo Diferente",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Algo Diferente.mp3",
#         "img": "music/Jhamy Deja-Vu - Algo Diferente_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Chaverot (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Chaverot (Remastered).mp3",
#         "img": "music/Los Zafiros - Chaverot (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "TEST DRIVE",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - TEST DRIVE.mp3",
#         "img": "music/Joji - TEST DRIVE_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Demonios",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Demonios.mp3",
#         "img": "music/Estopa - Demonios_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Era",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/11 Estopa - Era.mp3",
#         "img": "music/11 Estopa - Era_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Caminadora",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Los Zafiros - La Caminadora.mp3",
#         "img": "music/Los Zafiros - La Caminadora_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Janine 3",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/12 Camille - Janine 3.mp3",
#         "img": "music/12 Camille - Janine 3_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "King Kunta",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - King Kunta.mp3",
#         "img": "music/Kendrick Lamar - King Kunta_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Echate p'all\u00e1, echate p'aca",
#         "artist": "Habana Blues",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/07 Habana Blues - Echate p'all\u00e1, echate p'aca.mp3",
#         "img": "music/07 Habana Blues - Echate p'all\u00e1, echate p'aca_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La caminadora (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Hermosa Habana (Remastered) CD 1 TRACK 1 (320).mp3",
#         "img": "music/Hermosa Habana (Remastered) CD 1 TRACK 1 (320)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Estrella Fugaz",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Estrella Fugaz.mp3",
#         "img": "music/Estopa - Estrella Fugaz_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Como Mata el Viento Norte",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "La M\u00e1quina De Hacer P\u00e1jaros",
#         "address": "music/La Maquina De Hacer P\u00e1jaros - Como Mata el Viento Norte.mp3",
#         "img": "music/La Maquina De Hacer P\u00e1jaros - Como Mata el Viento Norte_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hoy Todo El Hielo En La Ciudad",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Hoy Todo El Hielo En La Ciudad.mp3",
#         "img": "music/Almendra - Hoy Todo El Hielo En La Ciudad_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Free Bird",
#         "artist": "Lynyrd Skynyrd",
#         "genre": "Rock",
#         "album": "(Pronounced 'Leh-'N\u00e9rd 'Skin-'N\u00e9rd)",
#         "address": "music/Lynyrd Skynyrd - Free Bird.mp3",
#         "img": "music/Lynyrd Skynyrd - Free Bird_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Quiero Verlas M\u00e1s",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/03 Estopa - No Quiero Verlas M\u00e1s.mp3",
#         "img": "music/03 Estopa - No Quiero Verlas M\u00e1s_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Black Dog (2012 Remaster)",
#         "artist": "Led Zeppelin",
#         "genre": "Rock",
#         "album": "Led Zeppelin IV (Deluxe Edition; Remaster)",
#         "address": "music/Led Zeppelin - Black Dog (2012 Remaster).mp3",
#         "img": "music/Led Zeppelin - Black Dog (2012 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sappy (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Sappy (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - Sappy (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Wana",
#         "artist": "Nour",
#         "genre": "null",
#         "album": "Wana",
#         "address": "music/Nour - Wana.mp3",
#         "img": "music/Nour - Wana_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pastillas de Freno",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Pastillas de Freno.mp3",
#         "img": "music/Estopa - Pastillas de Freno_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Qu\u00e9 Se Puede Hacer Con el Amor",
#         "artist": "Silvio Rodr\u00edguez",
#         "genre": "Singer & Songwriter",
#         "album": "Al Final de Este Viaje...",
#         "address": "music/Silvio Rodr\u00edguez - Qu\u00e9 Se Puede Hacer Con el Amor.mp3",
#         "img": "music/Silvio Rodr\u00edguez - Qu\u00e9 Se Puede Hacer Con el Amor_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cae El Sol (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Canci\u00f3n Animal (Remastered)",
#         "address": "music/Soda Stereo - Cae El Sol (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Cae El Sol (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Languis (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Doble Vida (Remastered)",
#         "address": "music/Soda Stereo - Languis (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Languis (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Institutionalized",
#         "artist": "Kendrick Lamar, Bilal, Anna Wise, Snoop Dogg",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick_Lamar,_Bilal,_Anna_Wise,_Snoop_Dogg_Institutionalized.mp3",
#         "img": "music/Kendrick_Lamar,_Bilal,_Anna_Wise,_Snoop_Dogg_Institutionalized_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Te Anim\u00e1s A Despegar",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Charly Garc\u00eda - No Te Anim\u00e1s A Despegar.mp3",
#         "img": "music/Charly Garc\u00eda - No Te Anim\u00e1s A Despegar_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hello User",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - Hello User.mp3",
#         "img": "music/Descartes A Kant - Hello User_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Amparo - Epoca Rosa (Buleria)",
#         "artist": "Diego \"El Cigala\"",
#         "genre": "null",
#         "album": "Picasso En Mis Ojos",
#         "address": "music/Diego  El Cigala  - Amparo - Epoca Rosa (Buleria).mp3",
#         "img": "music/Diego  El Cigala  - Amparo - Epoca Rosa (Buleria)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Guren No Yumiya",
#         "artist": "Linked Horizon",
#         "genre": "Elokuvat/Pelit",
#         "album": "Jiyuu Eno Shingeki",
#         "address": "music/01 Linked Horizon - Guren No Yumiya.mp3",
#         "img": "music/01 Linked Horizon - Guren No Yumiya_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cementerio Club",
#         "artist": "Pescado Rabioso",
#         "genre": "Rock",
#         "album": "Artaud",
#         "address": "music/Pescado Rabioso - Cementerio Club.mp3",
#         "img": "music/Pescado Rabioso - Cementerio Club_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "gm / outro",
#         "artist": "Nour",
#         "genre": "null",
#         "album": "daydreamer",
#         "address": "music/Nour - gm _ outro.mp3",
#         "img": "music/Nour - gm _ outro_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Clima Tropical",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Clima Tropical.mp3",
#         "img": "music/Canserbero - Clima Tropical_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Destrangis in the Night",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Destrangis in the Night.mp3",
#         "img": "music/Estopa - Destrangis in the Night_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Te Hacen Falta Vitaminas (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Soda Stereo (Remastered)",
#         "address": "music/Soda Stereo - Te Hacen Falta Vitaminas (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Te Hacen Falta Vitaminas (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pa' Descargar",
#         "artist": "Toques del R\u00edo",
#         "genre": "Lateinamerikanische Musik",
#         "album": "P\u00e1 Que Te Sosiegues",
#         "address": "music/03 Toques del R\u00edo - Pa' Descargar.mp3",
#         "img": "music/03 Toques del R\u00edo - Pa' Descargar_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Siempre Hay Soluci\u00f3n",
#         "artist": "X Alfonso",
#         "genre": "Alternative & Indie Pop & Indie Rock & Electro & Chill Out/Trip-Hop/Lounge & Rap/Hip Hop",
#         "album": "Siempre Hay Soluci\u00f3n",
#         "address": "music/X Alfonso - Siempre Hay Soluci\u00f3n.mp3",
#         "img": "music/X Alfonso - Siempre Hay Soluci\u00f3n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Es Pico",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - Es Pico.mp3",
#         "img": "music/Canserbero - Es Pico_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Jolie bruine",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/17 Camille - Jolie bruine.mp3",
#         "img": "music/17 Camille - Jolie bruine_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Abrazo de Soledad",
#         "artist": "Toques del R\u00edo",
#         "genre": "Latinalainen musiikki",
#         "album": "P\u00e1 Que Te Sosiegues",
#         "address": "music/06 Toques del R\u00edo - Abrazo de Soledad.mp3",
#         "img": "music/06 Toques del R\u00edo - Abrazo de Soledad_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Nada en el Mundo",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Real World",
#         "address": "music/X Alfonso - Nada en el Mundo.mp3",
#         "img": "music/X Alfonso - Nada en el Mundo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sin Sobresaltos (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Pop & Rock & Latin Music",
#         "album": "Signos (Remastered)",
#         "address": "music/Soda Stereo - Sin Sobresaltos (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Sin Sobresaltos (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Fuente de Energia",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Fuente de Energia.mp3",
#         "img": "music/Estopa - Fuente de Energia_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Americanos",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Americanos.mp3",
#         "img": "music/Canserbero - Americanos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tanta Tinta Tonta",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Tanta Tinta Tonta.mp3",
#         "img": "music/Estopa - Tanta Tinta Tonta_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hasta Precisar el Aire",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Hasta Precisar el Aire.mp3",
#         "img": "music/Kamankola - Hasta Precisar el Aire_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sobredosis De T.V. (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Ruido Blanco (Remastered)",
#         "address": "music/Soda Stereo - Sobredosis de T.V. (Remasterizado 2007) (1).mp3",
#         "img": "music/Soda Stereo - Sobredosis de T.V. (Remasterizado 2007) (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Necesito Medicaci\u00f3n",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Necesito Medicaci\u00f3n.mp3",
#         "img": "music/Estopa - Necesito Medicaci\u00f3n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "CAN'T GET OVER YOU (feat. Clams Casino)",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - CAN T GET OVER YOU (feat. Clams Casino).mp3",
#         "img": "music/Joji - CAN T GET OVER YOU (feat. Clams Casino)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Man\u00ed",
#         "artist": "Toques del R\u00edo",
#         "genre": "Latinalainen musiikki",
#         "album": "P\u00e1 Que Te Sosiegues",
#         "address": "music/10 Toques del R\u00edo - Man\u00ed.mp3",
#         "img": "music/10 Toques del R\u00edo - Man\u00ed_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "God Knows I'm Good (2015 Remaster)",
#         "artist": "David Bowie",
#         "genre": "Pop",
#         "album": "David Bowie (aka Space Oddity) (2015 Remaster)",
#         "address": "music/David Bowie - God Knows I'm Good (2015 Remaster).mp3",
#         "img": "music/David Bowie - God Knows I'm Good (2015 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Y en un Espejo Vi",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - Y en un Espejo Vi.mp3",
#         "img": "music/Canserbero - Y en un Espejo Vi_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Quiero Verla M\u00e1s",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/09 Estopa - No Quiero Verla M\u00e1s.mp3",
#         "img": "music/09 Estopa - No Quiero Verla M\u00e1s_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "En La Ciudad De La Furia (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - En La Ciudad De La Furia (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - En La Ciudad De La Furia (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "KICK BACK",
#         "artist": "Kenshi Yonezu",
#         "genre": "null",
#         "album": "KICK BACK",
#         "address": "music/Kenshi Yonezu - KICK BACK.mp3",
#         "img": "music/Kenshi Yonezu - KICK BACK_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Alabao",
#         "artist": "Cimafunk",
#         "genre": "null",
#         "album": "Terapia",
#         "address": "music/Cimafunk - Alabao.mp3",
#         "img": "music/Cimafunk - Alabao_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Wesley's Theory",
#         "artist": "Kendrick Lamar, George Clinton, Thundercat",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick_Lamar,_George_Clinton,_Thundercat_Wesley's_Theory.mp3",
#         "img": "music/Kendrick_Lamar,_George_Clinton,_Thundercat_Wesley's_Theory_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Misty Mountain Hop (2012 Remaster)",
#         "artist": "Led Zeppelin",
#         "genre": "Rock",
#         "album": "Led Zeppelin IV (Deluxe Edition; Remaster)",
#         "address": "music/Led Zeppelin - Misty Mountain Hop (2012 Remaster).mp3",
#         "img": "music/Led Zeppelin - Misty Mountain Hop (2012 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Siempre Hay Soluci\u00f3n",
#         "artist": "X Alfonso",
#         "genre": "Alternative & Indie Pop & Indie Rock & Electro & Chill Out/Trip-Hop/Lounge & Rap/Hip Hop",
#         "album": "Siempre Hay Soluci\u00f3n",
#         "address": "music/X Alfonso - Siempre Hay Soluci\u00f3n (1).mp3",
#         "img": "music/X Alfonso - Siempre Hay Soluci\u00f3n (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "ATTENTION",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - ATTENTION.mp3",
#         "img": "music/Joji - ATTENTION_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Baby carni bird",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/06 Camille - Baby carni bird.mp3",
#         "img": "music/06 Camille - Baby carni bird_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Going to California (2012 Remaster)",
#         "artist": "Led Zeppelin",
#         "genre": "Rock",
#         "album": "Led Zeppelin IV (Deluxe Edition; Remaster)",
#         "address": "music/Led Zeppelin - Going to California (2012 Remaster).mp3",
#         "img": "music/Led Zeppelin - Going to California (2012 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tema de la Esperanza",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Los Zafiros - Tema de la Esperanza.mp3",
#         "img": "music/Los Zafiros - Tema de la Esperanza_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Total Interferencia",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Charly Garc\u00eda - Total Interferencia.mp3",
#         "img": "music/Charly Garc\u00eda - Total Interferencia_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Oye Nicola",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Los Zafiros - Oye Nicola.mp3",
#         "img": "music/Los Zafiros - Oye Nicola_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Santa Barbara",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Los Zafiros - Santa Barbara.mp3",
#         "img": "music/Los Zafiros - Santa Barbara_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Off to the Side",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Off to the Side.mp3",
#         "img": "music/L Imp\u00e9ratrice - Off to the Side_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "SLOW DANCING IN THE DARK",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - SLOW DANCING IN THE DARK.mp3",
#         "img": "music/Joji - SLOW DANCING IN THE DARK_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Boletos, Pases Y Abonos",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "La M\u00e1quina De Hacer P\u00e1jaros",
#         "address": "music/La Maquina De Hacer P\u00e1jaros - Boletos, Pases Y Abonos.mp3",
#         "img": "music/La Maquina De Hacer P\u00e1jaros - Boletos, Pases Y Abonos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Fuente de Energia",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/02 Estopa - Fuente de Energia.mp3",
#         "img": "music/02 Estopa - Fuente de Energia_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Promesas Sobre El Bidet",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Piano Bar CD 1 TRACK 2 (320).mp3",
#         "img": "music/Piano Bar CD 1 TRACK 2 (320)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Chalam\u00e1n (Remastered)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los Abuelos de la Nada - Chalam\u00e1n (Remastered).mp3",
#         "img": "music/Los Abuelos de la Nada - Chalam\u00e1n (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sweet",
#         "artist": "Cigarettes After Sex",
#         "genre": "Alternative",
#         "album": "Cigarettes After Sex",
#         "address": "music/06 Cigarettes After Sex - Sweet.mp3",
#         "img": "music/06 Cigarettes After Sex - Sweet_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Paloma - Olivo (Fandangos)",
#         "artist": "Diego \"El Cigala\"",
#         "genre": "null",
#         "album": "Picasso En Mis Ojos",
#         "address": "music/Diego  El Cigala  - La Paloma - Olivo (Fandangos).mp3",
#         "img": "music/Diego  El Cigala  - La Paloma - Olivo (Fandangos)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Penas Con Rumba",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Penas Con Rumba.mp3",
#         "img": "music/Estopa - Penas Con Rumba_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Trop sensible",
#         "artist": "ZAZ",
#         "genre": "Pop",
#         "album": "Zaz",
#         "address": "music/05 ZAZ - Trop sensible.mp3",
#         "img": "music/05 ZAZ - Trop sensible_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Rock and Roll (2012 Remaster)",
#         "artist": "Led Zeppelin",
#         "genre": "Rock",
#         "album": "Led Zeppelin IV (Deluxe Edition; Remaster)",
#         "address": "music/Led Zeppelin - Rock and Roll (2012 Remaster).mp3",
#         "img": "music/Led Zeppelin - Rock and Roll (2012 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Exiliado en el Lavabo",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/07 Estopa - Exiliado en el Lavabo.mp3",
#         "img": "music/07 Estopa - Exiliado en el Lavabo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Chan chan",
#         "artist": "Compay Segundo",
#         "genre": "Latin Music",
#         "album": "Gracias Compay (The Definitive Collection)",
#         "address": "music/Compay Segundo - Chan chan.mp3",
#         "img": "music/Compay Segundo - Chan chan_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "You Knew This Would Happen",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - You Knew This Would Happen.mp3",
#         "img": "music/Descartes A Kant - You Knew This Would Happen_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Lucia",
#         "artist": "Joan Manuel Serrat",
#         "genre": "Pop & Rock",
#         "album": "24 Paginas Inolvidables",
#         "address": "music/Joan Manuel Serrat - Lucia.mp3",
#         "img": "music/Joan Manuel Serrat - Lucia_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vino Tinto",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Vino Tinto.mp3",
#         "img": "music/Estopa - Vino Tinto_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Guindilla Ardiente (Remastered 1995)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los_Abuelos_de_la_Nada_Guindilla_Ardiente_Remastered_1995.mp3",
#         "img": "music/Los_Abuelos_de_la_Nada_Guindilla_Ardiente_Remastered_1995_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Negative Creep",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Negative Creep.mp3",
#         "img": "music/Nirvana - Negative Creep_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Se Puede Pensar Como un Prisionero",
#         "artist": "X Alfonso",
#         "genre": "Electro & Chill Out/Trip-Hop/Lounge & Rap/Hip Hop",
#         "album": "No Se Puede Pensar Como un Prisionero",
#         "address": "music/X Alfonso - No Se Puede Pensar Como un Prisionero.mp3",
#         "img": "music/X Alfonso - No Se Puede Pensar Como un Prisionero_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pr\u00f3logo",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Pr\u00f3logo.mp3",
#         "img": "music/Canserbero - Pr\u00f3logo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Apocalypse",
#         "artist": "Cigarettes After Sex",
#         "genre": "Alternative",
#         "album": "Cigarettes After Sex",
#         "address": "music/04 Cigarettes After Sex - Apocalypse.mp3",
#         "img": "music/04 Cigarettes After Sex - Apocalypse_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No se vuelve atras",
#         "artist": "Cuba Libre",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/11 Cuba Libre - No se vuelve atras.mp3",
#         "img": "music/11 Cuba Libre - No se vuelve atras_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Self-F",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - Self-F.mp3",
#         "img": "music/Descartes A Kant - Self-F_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cambio",
#         "artist": "X Alfonso",
#         "genre": "Alternative",
#         "album": "Inside",
#         "address": "music/X Alfonso - Cambio.mp3",
#         "img": "music/X Alfonso - Cambio_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Bailala Bien",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Bailala Bien.mp3",
#         "img": "music/Habana Abierta - Bailala Bien_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Llov\u00eda",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - Llov\u00eda.mp3",
#         "img": "music/Canserbero - Llov\u00eda_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "An Occasional Dream (2015 Remaster)",
#         "artist": "David Bowie",
#         "genre": "Pop",
#         "album": "David Bowie (aka Space Oddity) (2015 Remaster)",
#         "address": "music/David Bowie - An Occasional Dream (2015 Remaster).mp3",
#         "img": "music/David Bowie - An Occasional Dream (2015 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Aceptas",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Aceptas.mp3",
#         "img": "music/Canserbero - Aceptas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Habana Blues",
#         "artist": "Habana Blues",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/04 Habana Blues - Habana Blues.mp3",
#         "img": "music/04 Habana Blues - Habana Blues_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sifting",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Sifting.mp3",
#         "img": "music/Nirvana - Sifting_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Alright",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - Alright.mp3",
#         "img": "music/Kendrick Lamar - Alright_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Color Humano",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Color Humano.mp3",
#         "img": "music/Almendra - Color Humano_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Anomalie bleue",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Anomalie bleue.mp3",
#         "img": "music/L Imp\u00e9ratrice - Anomalie bleue_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "En Camino (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Pop & Rock & Latin Music",
#         "album": "Signos (Remastered)",
#         "address": "music/Soda Stereo - En Camino (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - En Camino (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Algo",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Algo.mp3",
#         "img": "music/Kamankola - Algo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mediterraneo",
#         "artist": "Joan Manuel Serrat",
#         "genre": "Pop & International Pop & Latin Music",
#         "album": "Mediterr\u00e1neo",
#         "address": "music/Joan Manuel Serrat - Mediterraneo.mp3",
#         "img": "music/Joan Manuel Serrat - Mediterraneo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vivamos Juntos",
#         "artist": "TIerra Verde",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/15 TIerra Verde - Vivamos Juntos.mp3",
#         "img": "music/15 TIerra Verde - Vivamos Juntos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vida",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Vida.mp3",
#         "img": "music/Canserbero - Vida_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tomb\u00e9e pour la sc\u00e8ne",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Tomb\u00e9e pour la sc\u00e8ne.mp3",
#         "img": "music/L Imp\u00e9ratrice - Tomb\u00e9e pour la sc\u00e8ne_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mucho Gusto",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Mucho Gusto.mp3",
#         "img": "music/Canserbero - Mucho Gusto_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Blew (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Blew (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - Blew (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tema De Pototo (Para Saber Como Es La Soledad)",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Tema De Pototo (Para Saber Como Es La Soledad).mp3",
#         "img": "music/Almendra - Tema De Pototo (Para Saber Como Es La Soledad)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Jingle",
#         "artist": "Almendra",
#         "genre": "Alternative & Indie Rock & Pop & Rock & Hard Rock",
#         "album": "Vinyl Replica: Almendra 2",
#         "address": "music/Almendra - Jingle.mp3",
#         "img": "music/Almendra - Jingle_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Estoy Azulado (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Nada Personal (Remastered)",
#         "address": "music/Soda Stereo - Estoy Azulado (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Estoy Azulado (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Quand je marche",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/15 Camille - Quand je marche.mp3",
#         "img": "music/15 Camille - Quand je marche_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ir A M\u00e1s (Remastered)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los Abuelos de la Nada - Ir A M\u00e1s (Remastered).mp3",
#         "img": "music/Los Abuelos de la Nada - Ir A M\u00e1s (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "En El Borde (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Doble Vida (Remastered)",
#         "address": "music/Soda Stereo - En El Borde (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - En El Borde (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "En La Vereda Del Sol",
#         "artist": "Seru Giran",
#         "genre": "Rock",
#         "album": "Peperina",
#         "address": "music/08 Seru Giran - En La Vereda Del Sol.mp3",
#         "img": "music/08 Seru Giran - En La Vereda Del Sol_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "COME THRU",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - COME THRU.mp3",
#         "img": "music/Joji - COME THRU_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cuerpo Triste",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/08 Estopa - Cuerpo Triste.mp3",
#         "img": "music/08 Estopa - Cuerpo Triste_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ecos (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Nada Personal (Remastered)",
#         "address": "music/Soda Stereo - Ecos (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Ecos (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "About a Girl (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - About a Girl (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - About a Girl (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ke Pasa!?",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Ke Pasa!.mp3",
#         "img": "music/Estopa - Ke Pasa!_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Ritmo De Tus Ojos (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Doble Vida (Remastered)",
#         "address": "music/Soda Stereo - El Ritmo De Tus Ojos (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - El Ritmo De Tus Ojos (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ni pa Ti Ni pa M\u00ed",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/10 Estopa - Ni pa Ti Ni pa M\u00ed.mp3",
#         "img": "music/10 Estopa - Ni pa Ti Ni pa M\u00ed_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Afrodis\u00edacos (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Soda Stereo (Remastered)",
#         "address": "music/Soda Stereo - Afrodis\u00edacos (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Afrodis\u00edacos (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Aunque no Est\u00e9 de Moda",
#         "artist": "Silvio Rodr\u00edguez",
#         "genre": "Singer & Songwriter",
#         "album": "Al Final de Este Viaje...",
#         "address": "music/Silvio Rodr\u00edguez - Aunque no Est\u00e9 de Moda.mp3",
#         "img": "music/Silvio Rodr\u00edguez - Aunque no Est\u00e9 de Moda_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Each Time You Fall in Love",
#         "artist": "Cigarettes After Sex",
#         "genre": "Vaihtoehtoinen",
#         "album": "Cigarettes After Sex",
#         "address": "music/02 Cigarettes After Sex - Each Time You Fall in Love.mp3",
#         "img": "music/02 Cigarettes After Sex - Each Time You Fall in Love_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Y Tu Amor Es una Vieja Medalla",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "null",
#         "album": "Kamikaze",
#         "address": "music/Luis Alberto Spinetta - Y Tu Amor Es una Vieja Medalla.mp3",
#         "img": "music/Luis Alberto Spinetta - Y Tu Amor Es una Vieja Medalla_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Son Palabras, Son Mis Huellas",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "No Son Palabras, Son Mis Huellas",
#         "address": "music/X Alfonso - No Son Palabras, Son Mis Huellas.mp3",
#         "img": "music/X Alfonso - No Son Palabras, Son Mis Huellas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pesadilla",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/12 Estopa - Pesadilla.mp3",
#         "img": "music/12 Estopa - Pesadilla_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Supercher\u00eda",
#         "artist": "Pescado Rabioso",
#         "genre": "Rock",
#         "album": "Artaud",
#         "address": "music/Pescado Rabioso - Supercher\u00eda.mp3",
#         "img": "music/Pescado Rabioso - Supercher\u00eda_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Woman Sobbing",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - Woman Sobbing.mp3",
#         "img": "music/Descartes A Kant - Woman Sobbing_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Muchacha (Ojos De Papel)",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Muchacha (Ojos De Papel).mp3",
#         "img": "music/Almendra - Muchacha (Ojos De Papel)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Truly",
#         "artist": "Cigarettes After Sex",
#         "genre": "Vaihtoehtoinen",
#         "album": "Cigarettes After Sex",
#         "address": "music/08 Cigarettes After Sex - Truly.mp3",
#         "img": "music/08 Cigarettes After Sex - Truly_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Monstruos",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/08 Estopa - Monstruos.mp3",
#         "img": "music/08 Estopa - Monstruos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Young & Dumb",
#         "artist": "Cigarettes After Sex",
#         "genre": "Vaihtoehtoinen",
#         "album": "Cigarettes After Sex",
#         "address": "music/10 Cigarettes After Sex - Young   Dumb.mp3",
#         "img": "music/10 Cigarettes After Sex - Young   Dumb_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Press Any Key",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - Press Any Key.mp3",
#         "img": "music/Descartes A Kant - Press Any Key_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "L'\u00e9quilibriste",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - L \u00e9quilibriste.mp3",
#         "img": "music/L Imp\u00e9ratrice - L \u00e9quilibriste_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ojitos Rojos (Directo)",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Ojitos Rojos (Directo).mp3",
#         "img": "music/Estopa - Ojitos Rojos (Directo)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Luna Lunera",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/11 Estopa - Luna Lunera.mp3",
#         "img": "music/11 Estopa - Luna Lunera_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Space Oddity (2015 Remaster)",
#         "artist": "David Bowie",
#         "genre": "Pop",
#         "album": "David Bowie (aka Space Oddity) (2015 Remaster)",
#         "address": "music/David Bowie - Space Oddity (2015 Remaster).mp3",
#         "img": "music/David Bowie - Space Oddity (2015 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Floyd the Barber (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Floyd the Barber (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - Floyd the Barber (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ninguna Parte",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/04 Estopa - Ninguna Parte.mp3",
#         "img": "music/04 Estopa - Ninguna Parte_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Jardin del Olvido",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Jardin del Olvido.mp3",
#         "img": "music/Estopa - Jardin del Olvido_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Desempolvando",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/06 Estopa - Desempolvando.mp3",
#         "img": "music/06 Estopa - Desempolvando_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Soy Un Extra\u00f1o",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Clics Modernos",
#         "address": "music/Charly Garc\u00eda - No Soy Un Extra\u00f1o.mp3",
#         "img": "music/Charly Garc\u00eda - No Soy Un Extra\u00f1o_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cansado",
#         "artist": "Habana Blues",
#         "genre": "Elokuvat/Pelit",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/01 Habana Blues - Cansado.mp3",
#         "img": "music/01 Habana Blues - Cansado_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Jerem\u00edas 17-5",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - Jerem\u00edas 17-5.mp3",
#         "img": "music/Canserbero - Jerem\u00edas 17-5_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Unwashed and Somewhat Slightly Dazed (2015 Remaster)",
#         "artist": "David Bowie",
#         "genre": "Pop",
#         "album": "David Bowie (aka Space Oddity) (2015 Remaster)",
#         "address": "music/David_Bowie_Unwashed_and_Somewhat_Slightly_Dazed_2015_Remaster.mp3",
#         "img": "music/David_Bowie_Unwashed_and_Somewhat_Slightly_Dazed_2015_Remaster_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Amanecer",
#         "artist": "Habana Blues",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/08 Habana Blues - Amanecer.mp3",
#         "img": "music/08 Habana Blues - Amanecer_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Janine 2",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/09 Camille - Janine 2.mp3",
#         "img": "music/09 Camille - Janine 2_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Resumen de Noticias",
#         "artist": "Silvio Rodr\u00edguez",
#         "genre": "Singer & Songwriter",
#         "album": "Al Final de Este Viaje...",
#         "address": "music/Silvio Rodr\u00edguez - Resumen de Noticias.mp3",
#         "img": "music/Silvio Rodr\u00edguez - Resumen de Noticias_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Janine 1",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/04 Camille - Janine 1.mp3",
#         "img": "music/04 Camille - Janine 1_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Signos (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Alternative & Indie Pop & Indie Rock & Pop & Indie Pop/Folk & Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Signos (Remasterizado 2007) (1).mp3",
#         "img": "music/Soda Stereo - Signos (Remasterizado 2007) (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cerca De La Revolucion",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Piano Bar CD 1 TRACK 9 (320).mp3",
#         "img": "music/Piano Bar CD 1 TRACK 9 (320)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Un Mill\u00f3n De A\u00f1os Luz (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Un Mill\u00f3n De A\u00f1os Luz (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Un Mill\u00f3n De A\u00f1os Luz (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Spank Thru (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Spank Thru (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - Spank Thru (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Me Falta el Aliento",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/04 Estopa - Me Falta el Aliento.mp3",
#         "img": "music/04 Estopa - Me Falta el Aliento_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "School",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - School.mp3",
#         "img": "music/Nirvana - School_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Jugar al Despiste",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/09 Estopa - Jugar al Despiste.mp3",
#         "img": "music/09 Estopa - Jugar al Despiste_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mockingbird",
#         "artist": "Uma",
#         "genre": "null",
#         "album": "Bel\u2022li",
#         "address": "music/Uma - Mockingbird.mp3",
#         "img": "music/Uma - Mockingbird_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Rock And Roll",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "La M\u00e1quina De Hacer P\u00e1jaros",
#         "address": "music/La Maquina De Hacer P\u00e1jaros - Rock And Roll.mp3",
#         "img": "music/La Maquina De Hacer P\u00e1jaros - Rock And Roll_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Standing in the Sun",
#         "artist": "Uma",
#         "genre": "null",
#         "album": "Bel\u2022li",
#         "address": "music/Uma - Standing in the Sun.mp3",
#         "img": "music/Uma - Standing in the Sun_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Existes (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Pop & Rock & Latin Music",
#         "album": "Signos (Remastered)",
#         "address": "music/Soda Stereo - No Existes (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - No Existes (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Trafico de Luz",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Trafico de Luz.mp3",
#         "img": "music/Kamankola - Trafico de Luz_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Je veux",
#         "artist": "ZAZ",
#         "genre": "Pop",
#         "album": "Zaz",
#         "address": "music/02 ZAZ - Je veux.mp3",
#         "img": "music/02 ZAZ - Je veux_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Bossa cubana (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Bossa cubana (Remastered).mp3",
#         "img": "music/Los Zafiros - Bossa cubana (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ametrallame",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Ametrallame.mp3",
#         "img": "music/Kamankola - Ametrallame_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Justice",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - No Justice.mp3",
#         "img": "music/Canserbero - No Justice_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Besando Tu Corazon",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Real World",
#         "address": "music/X Alfonso - Besando Tu Corazon.mp3",
#         "img": "music/X Alfonso - Besando Tu Corazon_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "\u00c1guila de Trueno (Parte I)",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "null",
#         "album": "Kamikaze",
#         "address": "music/Luis Alberto Spinetta - \u00c1guila de Trueno (Parte I).mp3",
#         "img": "music/Luis Alberto Spinetta - \u00c1guila de Trueno (Parte I)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Familia, la Propiedad Privada y el Amor",
#         "artist": "Silvio Rodr\u00edguez",
#         "genre": "Singer & Songwriter",
#         "album": "Al Final de Este Viaje...",
#         "address": "music/Silvio_Rodr\u00edguez_La_Familia,_la_Propiedad_Privada_y_el_Amor.mp3",
#         "img": "music/Silvio_Rodr\u00edguez_La_Familia,_la_Propiedad_Privada_y_el_Amor_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cuando Yo la Conoci",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Locura Azul - Original Soundtrack CD 1 TRACK 6 (320).mp3",
#         "img": "music/Locura Azul - Original Soundtrack CD 1 TRACK 6 (320)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Como Soy Cubano",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Como Soy Cubano.mp3",
#         "img": "music/Habana Abierta - Como Soy Cubano_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Te Vi Te Vi",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Te Vi Te Vi.mp3",
#         "img": "music/Estopa - Te Vi Te Vi_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Paper Cuts",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Paper Cuts.mp3",
#         "img": "music/Nirvana - Paper Cuts_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Rebelion",
#         "artist": "Escape",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/14 Escape - Rebelion.mp3",
#         "img": "music/14 Escape - Rebelion_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "T\u00e9 Para 3 (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Canci\u00f3n Animal (Remastered)",
#         "address": "music/Soda Stereo - T\u00e9 Para 3 (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - T\u00e9 Para 3 (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pueblo Blanco",
#         "artist": "Joan Manuel Serrat",
#         "genre": "Pop & International Pop & Latin Music",
#         "album": "Mediterr\u00e1neo",
#         "address": "music/Joan Manuel Serrat - Pueblo Blanco.mp3",
#         "img": "music/Joan Manuel Serrat - Pueblo Blanco_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Un Nombre de Mujer",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Locura Azul - Original Soundtrack CD 1 TRACK 8 (320).mp3",
#         "img": "music/Locura Azul - Original Soundtrack CD 1 TRACK 8 (320)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ella Tambi\u00e9n",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "Rock",
#         "album": "Kamikaze",
#         "address": "music/02 Luis Alberto Spinetta - Ella Tambi\u00e9n.mp3",
#         "img": "music/02 Luis Alberto Spinetta - Ella Tambi\u00e9n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Kaikai Kitan",
#         "artist": "Eve",
#         "genre": "null",
#         "album": "Kaikai Kitan",
#         "address": "music/Eve - Kaikai Kitan.mp3",
#         "img": "music/Eve - Kaikai Kitan_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pride",
#         "artist": "Uma",
#         "genre": "null",
#         "album": "Bel\u2022li",
#         "address": "music/Uma - Pride.mp3",
#         "img": "music/Uma - Pride_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Prends garde \u00e0 ta langue",
#         "artist": "ZAZ",
#         "genre": "Pop",
#         "album": "Zaz",
#         "address": "music/06 ZAZ - Prends garde \u00e0 ta langue.mp3",
#         "img": "music/06 ZAZ - Prends garde \u00e0 ta langue_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Memory of a Free Festival (2015 Remaster)",
#         "artist": "David Bowie",
#         "genre": "Pop",
#         "album": "David Bowie (aka Space Oddity) (2015 Remaster)",
#         "address": "music/David Bowie - Memory of a Free Festival (2015 Remaster).mp3",
#         "img": "music/David Bowie - Memory of a Free Festival (2015 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "\u00bfCambiar\u00e1?",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Reverse",
#         "address": "music/X Alfonso -  Cambiar\u00e1.mp3",
#         "img": "music/X Alfonso -  Cambiar\u00e1_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Que Se Puede Hacer Salvo Ver Peliculas",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "Peliculas",
#         "address": "music/La_Maquina_De_Hacer_P\u00e1jaros_Que_Se_Puede_Hacer_Salvo_Ver_P.mp3",
#         "img": "music/La_Maquina_De_Hacer_P\u00e1jaros_Que_Se_Puede_Hacer_Salvo_Ver_P_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Siempre Happy",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Siempre Happy.mp3",
#         "img": "music/Habana Abierta - Siempre Happy_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Deseos en Penumbras",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Deseos en Penumbras.mp3",
#         "img": "music/Jhamy Deja-Vu - Deseos en Penumbras_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Dos Cero Uno",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Clics Modernos",
#         "address": "music/Charly Garc\u00eda - Dos Cero Uno.mp3",
#         "img": "music/Charly Garc\u00eda - Dos Cero Uno_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Dime Qu\u00e9 Hay Que Hacer",
#         "artist": "X Alfonso",
#         "genre": "Rap/Hip Hop",
#         "album": "Dime Qu\u00e9 Hay Que Hacer",
#         "address": "music/X Alfonso - Dime Qu\u00e9 Hay Que Hacer.mp3",
#         "img": "music/X Alfonso - Dime Qu\u00e9 Hay Que Hacer_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cygnet Committee (2015 Remaster)",
#         "artist": "David Bowie",
#         "genre": "Pop",
#         "album": "David Bowie (aka Space Oddity) (2015 Remaster)",
#         "address": "music/David Bowie - Cygnet Committee (2015 Remaster).mp3",
#         "img": "music/David Bowie - Cygnet Committee (2015 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vino Tinto",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/05 Estopa - Vino Tinto.mp3",
#         "img": "music/05 Estopa - Vino Tinto_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "the WORLD",
#         "artist": "Nightmare",
#         "genre": "null",
#         "album": "10th anniversary album Historical\uff5eThe highest NIGHTMARE\uff5e",
#         "address": "music/Nightmare - the WORLD.mp3",
#         "img": "music/Nightmare - the WORLD_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "(En) El S\u00e9ptimo D\u00eda (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Canci\u00f3n Animal (Remastered)",
#         "address": "music/Soda Stereo - (En) El S\u00e9ptimo D\u00eda (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - (En) El S\u00e9ptimo D\u00eda (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Jos\u00e9 Mercado",
#         "artist": "Seru Giran",
#         "genre": "Rock",
#         "album": "Peperina",
#         "address": "music/09 Seru Giran - Jos\u00e9 Mercado.mp3",
#         "img": "music/09 Seru Giran - Jos\u00e9 Mercado_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Raja de Tu Falda",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/06 Estopa - La Raja de Tu Falda.mp3",
#         "img": "music/06 Estopa - La Raja de Tu Falda_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Asere \u00bfQu\u00e9 Vol\u00e1?",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Asere  Qu\u00e9 Vol\u00e1.mp3",
#         "img": "music/Habana Abierta - Asere  Qu\u00e9 Vol\u00e1_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Haruka Kanata",
#         "artist": "ASIAN KUNG-FU GENERATION",
#         "genre": "null",
#         "album": "Destructive Amplifier",
#         "address": "music/ASIAN KUNG-FU GENERATION - Haruka Kanata.mp3",
#         "img": "music/ASIAN KUNG-FU GENERATION - Haruka Kanata_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Rosario",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Rosario.mp3",
#         "img": "music/Kamankola - Rosario_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mambo Nro. 0",
#         "artist": "Toques del R\u00edo",
#         "genre": "Latinalainen musiikki",
#         "album": "P\u00e1 Que Te Sosiegues",
#         "address": "music/07 Toques del R\u00edo - Mambo Nro. 0.mp3",
#         "img": "music/07 Toques del R\u00edo - Mambo Nro. 0_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Siento que...",
#         "artist": "X Alfonso",
#         "genre": "Electro & Chill Out/Trip-Hop/Lounge & Rap/Hip Hop",
#         "album": "Siento que...",
#         "address": "music/X Alfonso - Siento que... (1).mp3",
#         "img": "music/X Alfonso - Siento que... (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "We Are! (ONE PIECE)",
#         "artist": "Kitadani Hiroshi",
#         "genre": "null",
#         "album": "[Anison Live Taizenshu] Netsuretu! Anison Spirit Anitama Live Vol.1 in AJF 2004",
#         "address": "music/Kitadani Hiroshi - We Are! (ONE PIECE).mp3",
#         "img": "music/Kitadani Hiroshi - We Are! (ONE PIECE)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Graceless",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - Graceless.mp3",
#         "img": "music/Descartes A Kant - Graceless_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Raros Peinados Nuevos",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Charly Garc\u00eda - Raros Peinados Nuevos.mp3",
#         "img": "music/Charly Garc\u00eda - Raros Peinados Nuevos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Canci\u00f3n Del Elegido",
#         "artist": "Silvio Rodr\u00edguez",
#         "genre": "Singer & Songwriter",
#         "album": "Al Final de Este Viaje...",
#         "address": "music/Silvio Rodr\u00edguez - Canci\u00f3n Del Elegido.mp3",
#         "img": "music/Silvio Rodr\u00edguez - Canci\u00f3n Del Elegido_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tant d'amour perdu",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Tant d amour perdu.mp3",
#         "img": "music/L Imp\u00e9ratrice - Tant d amour perdu_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vientos de Tormenta",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/11 Estopa - Vientos de Tormenta.mp3",
#         "img": "music/11 Estopa - Vientos de Tormenta_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Por Qu\u00e9 No Puedo Ser Del Jet Set? (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Soda Stereo (Remastered)",
#         "address": "music/Soda_Stereo_Por_Qu\u00e9_No_Puedo_Ser_Del_Jet_Set_Remasterizado_2007.mp3",
#         "img": "music/Soda_Stereo_Por_Qu\u00e9_No_Puedo_Ser_Del_Jet_Set_Remasterizado_2007_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "\u00d3leo de Mujer Con Sombrero",
#         "artist": "Silvio Rodr\u00edguez",
#         "genre": "Singer & Songwriter",
#         "album": "Al Final de Este Viaje...",
#         "address": "music/Silvio Rodr\u00edguez - \u00d3leo de Mujer Con Sombrero.mp3",
#         "img": "music/Silvio Rodr\u00edguez - \u00d3leo de Mujer Con Sombrero_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Bajan",
#         "artist": "Pescado Rabioso",
#         "genre": "Rock",
#         "album": "Artaud",
#         "address": "music/Pescado Rabioso - Bajan.mp3",
#         "img": "music/Pescado Rabioso - Bajan_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Me Voy",
#         "artist": "Cimafunk",
#         "genre": "null",
#         "album": "Terapia",
#         "address": "music/Cimafunk - Me Voy.mp3",
#         "img": "music/Cimafunk - Me Voy_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Fin de Semana",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Fin de Semana.mp3",
#         "img": "music/Estopa - Fin de Semana_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cara De Velocidad",
#         "artist": "Seru Giran",
#         "genre": "Rock",
#         "album": "Peperina",
#         "address": "music/04 Seru Giran - Cara De Velocidad.mp3",
#         "img": "music/04 Seru Giran - Cara De Velocidad_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Presenta\u00f1o",
#         "artist": "Toques del R\u00edo",
#         "genre": "Latinalainen musiikki",
#         "album": "P\u00e1 Que Te Sosiegues",
#         "address": "music/08 Toques del R\u00edo - Presenta\u00f1o.mp3",
#         "img": "music/08 Toques del R\u00edo - Presenta\u00f1o_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Nas\u00edo pa la Alegria",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Nas\u00edo pa la Alegria.mp3",
#         "img": "music/Estopa - Nas\u00edo pa la Alegria_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Fou",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Fou.mp3",
#         "img": "music/L Imp\u00e9ratrice - Fou_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Nuevos Trapos",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Clics Modernos",
#         "address": "music/Charly Garc\u00eda - Nuevos Trapos.mp3",
#         "img": "music/Charly Garc\u00eda - Nuevos Trapos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Lo Bueno No Sale Barato",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - Lo Bueno No Sale Barato.mp3",
#         "img": "music/Habana Abierta - Lo Bueno No Sale Barato_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Kamikaze",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "null",
#         "album": "Kamikaze",
#         "address": "music/Luis Alberto Spinetta - Kamikaze.mp3",
#         "img": "music/Luis Alberto Spinetta - Kamikaze_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Rumba como quiera (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Rumba como quiera (Remastered).mp3",
#         "img": "music/Los Zafiros - Rumba como quiera (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "School (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - School (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - School (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sin Permiso",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Reverse",
#         "address": "music/X Alfonso - Sin Permiso.mp3",
#         "img": "music/X Alfonso - Sin Permiso_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "De Coraz\u00f3n",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Reverse",
#         "address": "music/X Alfonso - De Coraz\u00f3n.mp3",
#         "img": "music/X Alfonso - De Coraz\u00f3n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Como Camar\u00f3n",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/10 Estopa - Como Camar\u00f3n.mp3",
#         "img": "music/10 Estopa - Como Camar\u00f3n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Haruka Kanata",
#         "artist": "ASIAN KUNG-FU GENERATION",
#         "genre": "null",
#         "album": "Destructive Amplifier",
#         "address": "music/ASIAN KUNG-FU GENERATION - Haruka Kanata (1).mp3",
#         "img": "music/ASIAN KUNG-FU GENERATION - Haruka Kanata (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "J'ai tort",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/16 Camille - J'ai tort.mp3",
#         "img": "music/16 Camille - J'ai tort_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tan Solo",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/13 Estopa - Tan Solo.mp3",
#         "img": "music/13 Estopa - Tan Solo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Gabinetes Espaciales",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Gabinetes Espaciales.mp3",
#         "img": "music/Almendra - Gabinetes Espaciales_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Blue Bird",
#         "artist": "Ikimonogakari",
#         "genre": "Aasialainen musiikki",
#         "album": "Chou Ikimonobakari Tennen Kinen Members Best Selection",
#         "address": "music/03 Ikimonogakari - Blue Bird.mp3",
#         "img": "music/03 Ikimonogakari - Blue Bird_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Rap Del Exilio",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Charly Garc\u00eda - Rap Del Exilio.mp3",
#         "img": "music/Charly Garc\u00eda - Rap Del Exilio_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tio Alberto",
#         "artist": "Joan Manuel Serrat",
#         "genre": "Pop & International Pop & Latin Music",
#         "album": "Mediterr\u00e1neo",
#         "address": "music/Joan Manuel Serrat - Tio Alberto.mp3",
#         "img": "music/Joan Manuel Serrat - Tio Alberto_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tilo",
#         "artist": "Toques del R\u00edo",
#         "genre": "Lateinamerikanische Musik",
#         "album": "P\u00e1 Que Te Sosiegues",
#         "address": "music/05 Toques del R\u00edo - Tilo.mp3",
#         "img": "music/05 Toques del R\u00edo - Tilo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Descatalogando",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/07 Estopa - Descatalogando.mp3",
#         "img": "music/07 Estopa - Descatalogando_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Diet\u00e9tico (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Soda Stereo (Remastered)",
#         "address": "music/Soda Stereo - Diet\u00e9tico (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Diet\u00e9tico (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ya No Me Acuerdo",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Ya No Me Acuerdo.mp3",
#         "img": "music/Estopa - Ya No Me Acuerdo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Martillos y Ruedas",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Martillos y Ruedas.mp3",
#         "img": "music/Canserbero - Martillos y Ruedas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Lagrimas tatuadas",
#         "artist": "Habana Blues",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/09 Habana Blues - Lagrimas tatuadas.mp3",
#         "img": "music/09 Habana Blues - Lagrimas tatuadas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "In Case You Didn't Know",
#         "artist": "Brett Young",
#         "genre": "Country",
#         "album": "Brett Young - EP",
#         "address": "music/Brett Young - In Case You Didn't Know.mp3",
#         "img": "music/Brett Young - In Case You Didn't Know_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Siento que...",
#         "artist": "X Alfonso",
#         "genre": "Electro & Chill Out/Trip-Hop/Lounge & Rap/Hip Hop",
#         "album": "Siento que...",
#         "address": "music/X Alfonso - Siento que....mp3",
#         "img": "music/X Alfonso - Siento que..._cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "\u00c9blouie par la nuit",
#         "artist": "ZAZ",
#         "genre": "Pop",
#         "album": "Zaz",
#         "address": "music/11 ZAZ - \u00c9blouie par la nuit.mp3",
#         "img": "music/11 ZAZ - \u00c9blouie par la nuit_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Blew",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Blew.mp3",
#         "img": "music/Nirvana - Blew_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Love Buzz (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Love Buzz (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - Love Buzz (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Scoff",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Scoff.mp3",
#         "img": "music/Nirvana - Scoff_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Fantasia Real",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Real World",
#         "address": "music/X Alfonso - Fantasia Real.mp3",
#         "img": "music/X Alfonso - Fantasia Real_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "XNXX",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - XNXX.mp3",
#         "img": "music/Joji - XNXX_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Era",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/07 Estopa - Era.mp3",
#         "img": "music/07 Estopa - Era_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Im\u00e1genes Retro (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Nada Personal (Remastered)",
#         "address": "music/Soda Stereo - Im\u00e1genes Retro (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Im\u00e1genes Retro (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Los Dinosaurios",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Clics Modernos",
#         "address": "music/Charly Garc\u00eda - Los Dinosaurios.mp3",
#         "img": "music/Charly Garc\u00eda - Los Dinosaurios_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Noticia",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Reverse",
#         "address": "music/X Alfonso - Noticia.mp3",
#         "img": "music/X Alfonso - Noticia_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "For Free? (Interlude)",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - For Free (Interlude).mp3",
#         "img": "music/Kendrick Lamar - For Free (Interlude)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ya No S\u00e9 Que Hacer Conmigo",
#         "artist": "El Cuarteto de Nos",
#         "genre": "null",
#         "album": "Raro",
#         "address": "music/El Cuarteto de Nos - Ya No S\u00e9 Que Hacer Conmigo.mp3",
#         "img": "music/El Cuarteto de Nos - Ya No S\u00e9 Que Hacer Conmigo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "John Wayne",
#         "artist": "Cigarettes After Sex",
#         "genre": "Vaihtoehtoinen",
#         "album": "Cigarettes After Sex",
#         "address": "music/09 Cigarettes After Sex - John Wayne.mp3",
#         "img": "music/09 Cigarettes After Sex - John Wayne_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pensando en Ti",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Pensando en Ti.mp3",
#         "img": "music/Canserbero - Pensando en Ti_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Como Palo Pa Candela",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Como Palo Pa Candela.mp3",
#         "img": "music/Kamankola - Como Palo Pa Candela_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Big Cheese",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Big Cheese.mp3",
#         "img": "music/Nirvana - Big Cheese_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "\u00danetenos",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - \u00danetenos.mp3",
#         "img": "music/Canserbero - \u00danetenos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "The Battle of Evermore (Remaster)",
#         "artist": "Led Zeppelin",
#         "genre": "Rock",
#         "album": "Led Zeppelin IV (Deluxe Edition)",
#         "address": "music/Led Zeppelin - The Battle of Evermore (Remaster).mp3",
#         "img": "music/Led Zeppelin - The Battle of Evermore (Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Malague\u00f1o - Azul (De Malaga Malague\u00f1ito)",
#         "artist": "Diego \"El Cigala\"",
#         "genre": "null",
#         "album": "Picasso En Mis Ojos",
#         "address": "music/Diego_El_Cigala_Malague\u00f1o_Azul_De_Malaga_Malague\u00f1ito.mp3",
#         "img": "music/Diego_El_Cigala_Malague\u00f1o_Azul_De_Malaga_Malague\u00f1ito_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cuando Pase El Temblor (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Alternative & Indie Pop & Indie Rock & Pop & Indie Pop/Folk & Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Cuando Pase El Temblor (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Cuando Pase El Temblor (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vuelvo a las Andadas",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Vuelvo a las Andadas.mp3",
#         "img": "music/Estopa - Vuelvo a las Andadas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Primer Trago",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - El Primer Trago.mp3",
#         "img": "music/Canserbero - El Primer Trago_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ser Vero",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - Ser Vero.mp3",
#         "img": "music/Canserbero - Ser Vero_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Paseo",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/12 Estopa - Paseo.mp3",
#         "img": "music/12 Estopa - Paseo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Evolucionando",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Evolucionando.mp3",
#         "img": "music/Jhamy Deja-Vu - Evolucionando_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Por Probar El Vino Y El Agua Salada",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "La M\u00e1quina De Hacer P\u00e1jaros",
#         "address": "music/La_Maquina_De_Hacer_P\u00e1jaros_Por_Probar_El_Vino_Y_El_Agua_S.mp3",
#         "img": "music/La_Maquina_De_Hacer_P\u00e1jaros_Por_Probar_El_Vino_Y_El_Agua_S_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sunsetz",
#         "artist": "Cigarettes After Sex",
#         "genre": "Alternative",
#         "album": "Cigarettes After Sex",
#         "address": "music/03 Cigarettes After Sex - Sunsetz.mp3",
#         "img": "music/03 Cigarettes After Sex - Sunsetz_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Persiana Americana (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Alternative & Indie Pop & Indie Rock & Pop & Indie Pop/Folk & Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Persiana Americana (Remasterizado 2007) (1).mp3",
#         "img": "music/Soda Stereo - Persiana Americana (Remasterizado 2007) (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Submarine",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Submarine.mp3",
#         "img": "music/L Imp\u00e9ratrice - Submarine_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pr\u00f3fugos (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Alternative & Indie Pop & Indie Rock & Pop & Indie Pop/Folk & Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Pr\u00f3fugos (Remasterizado 2007) (1).mp3",
#         "img": "music/Soda Stereo - Pr\u00f3fugos (Remasterizado 2007) (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Danza Rota (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Nada Personal (Remastered)",
#         "address": "music/Soda Stereo - Danza Rota (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Danza Rota (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "For Sale? (Interlude)",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - For Sale (Interlude).mp3",
#         "img": "music/Kendrick Lamar - For Sale (Interlude)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Felaci\u00f3n",
#         "artist": "Porno para Ricardo",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/13 Porno para Ricardo - Felaci\u00f3n.mp3",
#         "img": "music/13 Porno para Ricardo - Felaci\u00f3n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Por los Rios - Guitarra (Bulerias)",
#         "artist": "Diego \"El Cigala\"",
#         "genre": "null",
#         "album": "Picasso En Mis Ojos",
#         "address": "music/Diego  El Cigala  - Por los Rios - Guitarra (Bulerias).mp3",
#         "img": "music/Diego  El Cigala  - Por los Rios - Guitarra (Bulerias)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Stairway to Heaven (2012 Remaster)",
#         "artist": "Led Zeppelin",
#         "genre": "Rock",
#         "album": "Led Zeppelin IV (Deluxe Edition; Remaster)",
#         "address": "music/Led Zeppelin - Stairway to Heaven (2012 Remaster).mp3",
#         "img": "music/Led Zeppelin - Stairway to Heaven (2012 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mestizo",
#         "artist": "Almendra",
#         "genre": "Alternative & Indie Rock & Pop & Rock & Hard Rock",
#         "album": "Vinyl Replica: Almendra 2",
#         "address": "music/Almendra - Mestizo.mp3",
#         "img": "music/Almendra - Mestizo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pr\u00f3fugos (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Ruido Blanco (Remastered)",
#         "address": "music/Soda Stereo - Pr\u00f3fugos (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Pr\u00f3fugos (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Toma El Tren Hacia El Sur",
#         "artist": "Almendra",
#         "genre": "Alternative & Indie Rock & Pop & Rock & Hard Rock",
#         "album": "Vinyl Replica: Almendra 2",
#         "address": "music/Almendra - Toma El Tren Hacia El Sur.mp3",
#         "img": "music/Almendra - Toma El Tren Hacia El Sur_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cambio",
#         "artist": "X Alfonso",
#         "genre": "Alternative",
#         "album": "Inside",
#         "address": "music/X Alfonso - Cambio (1).mp3",
#         "img": "music/X Alfonso - Cambio (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Con Tus Labios",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Con Tus Labios.mp3",
#         "img": "music/Jhamy Deja-Vu - Con Tus Labios_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "alwan",
#         "artist": "Nour",
#         "genre": "null",
#         "album": "daydreamer",
#         "address": "music/Nour - alwan.mp3",
#         "img": "music/Nour - alwan_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "NO FUN",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - NO FUN.mp3",
#         "img": "music/Joji - NO FUN_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Scoff (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Scoff (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - Scoff (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Un Pedacito de Tu Tiempo",
#         "artist": "Toques del R\u00edo",
#         "genre": "Lateinamerikanische Musik",
#         "album": "P\u00e1 Que Te Sosiegues",
#         "address": "music/02 Toques del R\u00edo - Un Pedacito de Tu Tiempo.mp3",
#         "img": "music/02 Toques del R\u00edo - Un Pedacito de Tu Tiempo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La f\u00e9e",
#         "artist": "ZAZ",
#         "genre": "Pop",
#         "album": "Zaz",
#         "address": "music/04 ZAZ - La f\u00e9e.mp3",
#         "img": "music/04 ZAZ - La f\u00e9e_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vita-Set (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Ruido Blanco (Remastered)",
#         "address": "music/Soda Stereo - Vita-Set (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Vita-Set (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Jungla Gris",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Real World",
#         "address": "music/X Alfonso - Jungla Gris.mp3",
#         "img": "music/X Alfonso - Jungla Gris_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Habaneando",
#         "artist": "Habana Blues",
#         "genre": "Elokuvat/Pelit",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/02 Habana Blues - Habaneando.mp3",
#         "img": "music/02 Habana Blues - Habaneando_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Un D\u00eda en el Barrio",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - Un D\u00eda en el Barrio.mp3",
#         "img": "music/Canserbero - Un D\u00eda en el Barrio_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Pic Nic En El 4\u00b0 B (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Pic Nic En El 4\u00b0 B (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Pic Nic En El 4\u00b0 B (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Tiempo Es Dinero (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Soda Stereo (Remastered)",
#         "address": "music/Soda Stereo - El Tiempo Es Dinero (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - El Tiempo Es Dinero (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Nuestra \u00faltima cita (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Nuestra \u00faltima cita (Remastered).mp3",
#         "img": "music/Los Zafiros - Nuestra \u00faltima cita (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Reverse",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Reverse",
#         "address": "music/X Alfonso - Reverse.mp3",
#         "img": "music/X Alfonso - Reverse_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Piano Bar",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Charly Garc\u00eda - Piano Bar.mp3",
#         "img": "music/Charly Garc\u00eda - Piano Bar_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Gurenge",
#         "artist": "LiSA",
#         "genre": "null",
#         "album": "LEO-NiNE",
#         "address": "music/LiSA - Gurenge.mp3",
#         "img": "music/LiSA - Gurenge_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Se Va A Llamar Mi Amor",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Piano Bar",
#         "address": "music/Charly Garc\u00eda - No Se Va A Llamar Mi Amor.mp3",
#         "img": "music/Charly Garc\u00eda - No Se Va A Llamar Mi Amor_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Malabares",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/08 Estopa - Malabares.mp3",
#         "img": "music/08 Estopa - Malabares_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Alumina",
#         "artist": "Nightmare",
#         "genre": "null",
#         "album": "the WORLD/Alumina",
#         "address": "music/Nightmare - Alumina.mp3",
#         "img": "music/Nightmare - Alumina_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Final Caja Negra (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Pop & Rock & Latin Music",
#         "album": "Signos (Remastered)",
#         "address": "music/Soda Stereo - Final Caja Negra (Remasterizado 2007) (1).mp3",
#         "img": "music/Soda Stereo - Final Caja Negra (Remasterizado 2007) (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sueles Dejarme Solo (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Canci\u00f3n Animal (Remastered)",
#         "address": "music/Soda Stereo - Sueles Dejarme Solo (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Sueles Dejarme Solo (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Apag\u00f3n",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "La Calle Es Tuya?",
#         "address": "music/Estopa - Apag\u00f3n.mp3",
#         "img": "music/Estopa - Apag\u00f3n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Figuraci\u00f3n",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Figuraci\u00f3n.mp3",
#         "img": "music/Almendra - Figuraci\u00f3n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "En Las Calles De Costa Rica",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "Peliculas",
#         "address": "music/La Maquina De Hacer P\u00e1jaros - En Las Calles De Costa Rica.mp3",
#         "img": "music/La Maquina De Hacer P\u00e1jaros - En Las Calles De Costa Rica_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sin Gamul\u00e1n (Remastered)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los Abuelos de la Nada - Sin Gamul\u00e1n (Remastered).mp3",
#         "img": "music/Los Abuelos de la Nada - Sin Gamul\u00e1n (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sed\u00faceme",
#         "artist": "Habana Blues",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/03 Habana Blues - Sed\u00faceme.mp3",
#         "img": "music/03 Habana Blues - Sed\u00faceme_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Paraguayo Prensao",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Paraguayo Prensao.mp3",
#         "img": "music/Kamankola - Paraguayo Prensao_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Chaverot",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Los Zafiros - Chaverot.mp3",
#         "img": "music/Los Zafiros - Chaverot_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hace Falta So\u00f1ar",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Vida",
#         "address": "music/Canserbero - Hace Falta So\u00f1ar.mp3",
#         "img": "music/Canserbero - Hace Falta So\u00f1ar_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vertige",
#         "artist": "Camille",
#         "genre": "None",
#         "album": "Le fil",
#         "address": "music/10 Camille - Vertige.mp3",
#         "img": "music/10 Camille - Vertige_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "A Starosta, el Idiota",
#         "artist": "Pescado Rabioso",
#         "genre": "Rock",
#         "album": "Artaud",
#         "address": "music/Pescado Rabioso - A Starosta, el Idiota.mp3",
#         "img": "music/Pescado Rabioso - A Starosta, el Idiota_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Aprende to walk",
#         "artist": "Tribal",
#         "genre": "Filme/Videospiele",
#         "album": "Habana Blues (Banda Sonora Original)",
#         "address": "music/12 Tribal - Aprende to walk.mp3",
#         "img": "music/12 Tribal - Aprende to walk_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Zankokuna Tenshino Teeze",
#         "artist": "Mikuni Shimokawa",
#         "genre": "null",
#         "album": "Reprise -Anime Song Best-",
#         "address": "music/Mikuni Shimokawa - Zankokuna Tenshino Teeze.mp3",
#         "img": "music/Mikuni Shimokawa - Zankokuna Tenshino Teeze_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "i",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - i.mp3",
#         "img": "music/Kendrick Lamar - i_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "De M\u00fasica Ligera (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - De M\u00fasica Ligera (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - De M\u00fasica Ligera (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ten Fe",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Ten Fe.mp3",
#         "img": "music/Jhamy Deja-Vu - Ten Fe_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "These Walls",
#         "artist": "Kendrick Lamar, Bilal, Thundercat, Anna Wise",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar, Bilal, Thundercat, Anna Wise - These Walls.mp3",
#         "img": "music/Kendrick Lamar, Bilal, Thundercat, Anna Wise - These Walls_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Puedo Verme Mas",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "La M\u00e1quina De Hacer P\u00e1jaros",
#         "address": "music/La Maquina De Hacer P\u00e1jaros - No Puedo Verme Mas.mp3",
#         "img": "music/La Maquina De Hacer P\u00e1jaros - No Puedo Verme Mas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Run Run",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/10 Estopa - El Run Run.mp3",
#         "img": "music/10 Estopa - El Run Run_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Que No Es Lo Mismo",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Que No Es Lo Mismo.mp3",
#         "img": "music/Kamankola - Que No Es Lo Mismo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "YEAH RIGHT",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - YEAH RIGHT.mp3",
#         "img": "music/Joji - YEAH RIGHT_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ruta Perdedora",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "Peliculas",
#         "address": "music/La Maquina De Hacer P\u00e1jaros - Ruta Perdedora.mp3",
#         "img": "music/La Maquina De Hacer P\u00e1jaros - Ruta Perdedora_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cinema Verit\u00e9",
#         "artist": "Seru Giran",
#         "genre": "Rock",
#         "album": "Peperina",
#         "address": "music/07 Seru Giran - Cinema Verit\u00e9.mp3",
#         "img": "music/07 Seru Giran - Cinema Verit\u00e9_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "TELL ME WHY (TV version)",
#         "artist": "Penpals",
#         "genre": "null",
#         "album": "BERSERK Original Soundtrack",
#         "address": "music/Penpals - TELL ME WHY (TV version).mp3",
#         "img": "music/Penpals - TELL ME WHY (TV version)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Tako Tsubo",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Tako Tsubo.mp3",
#         "img": "music/L Imp\u00e9ratrice - Tako Tsubo_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Su Lagrima en Mis Ojos",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Su Lagrima en Mis Ojos.mp3",
#         "img": "music/Kamankola - Su Lagrima en Mis Ojos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Medita Sol (Remastered)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los Abuelos de la Nada - Medita Sol (Remastered).mp3",
#         "img": "music/Los Abuelos de la Nada - Medita Sol (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Que Suerte la M\u00eda",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/02 Estopa - Que Suerte la M\u00eda.mp3",
#         "img": "music/02 Estopa - Que Suerte la M\u00eda_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "La Novia de Superman",
#         "artist": "Habana Abierta",
#         "genre": "null",
#         "album": "Boomerang",
#         "address": "music/Habana Abierta - La Novia de Superman.mp3",
#         "img": "music/Habana Abierta - La Novia de Superman_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cerrando Circulos",
#         "artist": "Jhamy Deja-Vu",
#         "genre": "Reggae & Latin Music",
#         "album": "Perfecto Balance",
#         "address": "music/Jhamy Deja-Vu - Cerrando Circulos.mp3",
#         "img": "music/Jhamy Deja-Vu - Cerrando Circulos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hermosa Habana (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Hermosa Habana (Remastered).mp3",
#         "img": "music/Los Zafiros - Hermosa Habana (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Si Todos Creen",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Real World",
#         "address": "music/X Alfonso - Si Todos Creen.mp3",
#         "img": "music/X Alfonso - Si Todos Creen_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Reflexi\u00f3n",
#         "artist": "X Alfonso",
#         "genre": "Rap/Hip Hop",
#         "album": "Reflexi\u00f3n",
#         "address": "music/X Alfonso - Reflexi\u00f3n (1).mp3",
#         "img": "music/X Alfonso - Reflexi\u00f3n (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Cosas M\u00edas (Remastered)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "Rock & Latin Music",
#         "album": "Los Abuelos De La Nada 2",
#         "address": "music/Los Abuelos de la Nada - Cosas M\u00edas (Remastered).mp3",
#         "img": "music/Los Abuelos de la Nada - Cosas M\u00edas (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Lunes",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "Voces de Ultrarumba",
#         "address": "music/05 Estopa - Lunes.mp3",
#         "img": "music/05 Estopa - Lunes_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hablame de Amor",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Real World",
#         "address": "music/X Alfonso - Hablame de Amor.mp3",
#         "img": "music/X Alfonso - Hablame de Amor_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Downer",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Downer.mp3",
#         "img": "music/Nirvana - Downer_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "How Much A Dollar Cost",
#         "artist": "Kendrick Lamar, James Fauntleroy, Ronald Isley",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick_Lamar,_James_Fauntleroy,_Ronald_Isley_How_Much_A_Dollar.mp3",
#         "img": "music/Kendrick_Lamar,_James_Fauntleroy,_Ronald_Isley_How_Much_A_Dollar_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Rito (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Pop & Rock & Latin Music",
#         "album": "Signos (Remastered)",
#         "address": "music/Soda Stereo - El Rito (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - El Rito (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Romance - Mar (Sobresaltos de Plata)",
#         "artist": "Diego \"El Cigala\"",
#         "genre": "null",
#         "album": "Picasso En Mis Ojos",
#         "address": "music/Diego  El Cigala  - Romance - Mar (Sobresaltos de Plata).mp3",
#         "img": "music/Diego  El Cigala  - Romance - Mar (Sobresaltos de Plata)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Barro Tal Vez",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "Rock",
#         "album": "Kamikaze",
#         "address": "music/06 Luis Alberto Spinetta - Barro Tal Vez.mp3",
#         "img": "music/06 Luis Alberto Spinetta - Barro Tal Vez_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mis sentimientos (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Mis sentimientos (Remastered).mp3",
#         "img": "music/Los Zafiros - Mis sentimientos (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "WANTED U",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - WANTED U.mp3",
#         "img": "music/Joji - WANTED U_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El del Medio de los Chichos",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/12 Estopa - El del Medio de los Chichos.mp3",
#         "img": "music/12 Estopa - El del Medio de los Chichos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Me Dejan Salir",
#         "artist": "Charly Garc\u00eda",
#         "genre": "Rock",
#         "album": "Clics Modernos",
#         "address": "music/Charly Garc\u00eda - No Me Dejan Salir.mp3",
#         "img": "music/Charly Garc\u00eda - No Me Dejan Salir_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Casas Marcadas",
#         "artist": "Luis Alberto Spinetta",
#         "genre": "null",
#         "album": "Kamikaze",
#         "address": "music/Luis Alberto Spinetta - Casas Marcadas.mp3",
#         "img": "music/Luis Alberto Spinetta - Casas Marcadas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Era",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/03 Estopa - Era.mp3",
#         "img": "music/03 Estopa - Era_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sera Mi Sangre",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Sera Mi Sangre.mp3",
#         "img": "music/Kamankola - Sera Mi Sangre_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Canci\u00f3n Animal (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Canci\u00f3n Animal (Remastered)",
#         "address": "music/Soda Stereo - Canci\u00f3n Animal (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Canci\u00f3n Animal (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Lo Que Sangra (La C\u00fapula) (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Doble Vida (Remastered)",
#         "address": "music/Soda_Stereo_Lo_Que_Sangra_La_C\u00fapula_Remasterizado_2007.mp3",
#         "img": "music/Soda_Stereo_Lo_Que_Sangra_La_C\u00fapula_Remasterizado_2007_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "A Susana",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Reverse",
#         "address": "music/X Alfonso - A Susana.mp3",
#         "img": "music/X Alfonso - A Susana_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Juegos De Seducci\u00f3n (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Ruido Blanco (Remastered)",
#         "address": "music/Soda Stereo - Juegos De Seducci\u00f3n (Remasterizado 2007) (1).mp3",
#         "img": "music/Soda Stereo - Juegos De Seducci\u00f3n (Remasterizado 2007) (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Basta",
#         "artist": "Cimafunk",
#         "genre": "null",
#         "album": "Terapia",
#         "address": "music/Cimafunk - Basta.mp3",
#         "img": "music/Cimafunk - Basta_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Rutas Argentinas",
#         "artist": "Almendra",
#         "genre": "Alternative & Indie Rock & Pop & Rock & Hard Rock",
#         "album": "Vinyl Replica: Almendra 2",
#         "address": "music/Almendra - Rutas Argentinas.mp3",
#         "img": "music/Almendra - Rutas Argentinas_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hermano Perro",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Hermano Perro.mp3",
#         "img": "music/Almendra - Hermano Perro_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hood Politics",
#         "artist": "Kendrick Lamar",
#         "genre": "Rap/Hip Hop",
#         "album": "To Pimp A Butterfly",
#         "address": "music/Kendrick Lamar - Hood Politics.mp3",
#         "img": "music/Kendrick Lamar - Hood Politics_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Acuarela - Mujer (Solea)",
#         "artist": "Diego \"El Cigala\"",
#         "genre": "Pop",
#         "album": "Picasso En Mis Ojos",
#         "address": "music/10 Diego  El Cigala  - Acuarela - Mujer (Solea).mp3",
#         "img": "music/10 Diego  El Cigala  - Acuarela - Mujer (Solea)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Barquito de Papel",
#         "artist": "Joan Manuel Serrat",
#         "genre": "Pop & International Pop & Latin Music",
#         "album": "Mediterr\u00e1neo",
#         "address": "music/Joan Manuel Serrat - Barquito de Papel.mp3",
#         "img": "music/Joan Manuel Serrat - Barquito de Papel_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hemicraneal",
#         "artist": "Estopa",
#         "genre": "Vaihtoehtoinen",
#         "album": "Allenrok",
#         "address": "music/08 Estopa - Hemicraneal.mp3",
#         "img": "music/08 Estopa - Hemicraneal_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Intro (Live at Pine Street Theatre)",
#         "artist": "Nirvana",
#         "genre": "Alternative",
#         "album": "Bleach (Deluxe Edition)",
#         "address": "music/Nirvana - Intro (Live at Pine Street Theatre).mp3",
#         "img": "music/Nirvana - Intro (Live at Pine Street Theatre)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Conectao Respirando",
#         "artist": "Kamankola",
#         "genre": "Latin Music",
#         "album": "Hasta Precisar el Aire",
#         "address": "music/Kamankola - Conectao Respirando.mp3",
#         "img": "music/Kamankola - Conectao Respirando_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "H\u00e9matome",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - H\u00e9matome.mp3",
#         "img": "music/L Imp\u00e9ratrice - H\u00e9matome_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Qui\u00e9n Eres",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop",
#         "album": "Vida",
#         "address": "music/Canserbero - Qui\u00e9n Eres.mp3",
#         "img": "music/Canserbero - Qui\u00e9n Eres_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Un nombre de mujer (Remastered)",
#         "artist": "Los Zafiros",
#         "genre": "Latin Music",
#         "album": "Hermosa Habana (Remastered)",
#         "address": "music/Los Zafiros - Un nombre de mujer (Remastered).mp3",
#         "img": "music/Los Zafiros - Un nombre de mujer (Remastered)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Nada Personal (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Alternative & Indie Pop & Indie Rock & Pop & Indie Pop/Folk & Rock & Latin Music",
#         "album": "Me Ver\u00e1s Volver (Hits & M\u00e1s)",
#         "address": "music/Soda Stereo - Nada Personal (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Nada Personal (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Sex on Fire",
#         "artist": "Kings of Leon",
#         "genre": "Alternative",
#         "album": "Only By The Night",
#         "address": "music/Kings of Leon - Sex on Fire.mp3",
#         "img": "music/Kings of Leon - Sex on Fire_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Wild Eyed Boy from Freecloud (2015 Remaster)",
#         "artist": "David Bowie",
#         "genre": "Pop",
#         "album": "David Bowie (aka Space Oddity) (2015 Remaster)",
#         "address": "music/David Bowie - Wild Eyed Boy from Freecloud (2015 Remaster).mp3",
#         "img": "music/David Bowie - Wild Eyed Boy from Freecloud (2015 Remaster)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "The Mess We've Made",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - The Mess We ve Made.mp3",
#         "img": "music/Descartes A Kant - The Mess We ve Made_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Estoy Azulado (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Ruido Blanco (Remastered)",
#         "address": "music/Soda Stereo - Estoy Azulado (Remasterizado 2007) (1).mp3",
#         "img": "music/Soda Stereo - Estoy Azulado (Remasterizado 2007) (1)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "1990 (Mil Nueve Noventa) (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Canci\u00f3n Animal (Remastered)",
#         "address": "music/Soda Stereo - 1990 (Mil Nueve Noventa) (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - 1990 (Mil Nueve Noventa) (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Todas las Hojas Son del Viento",
#         "artist": "Pescado Rabioso",
#         "genre": "Rock",
#         "album": "Baladas y Canciones de Amor",
#         "address": "music/Pescado Rabioso - Todas las Hojas Son del Viento.mp3",
#         "img": "music/Pescado Rabioso - Todas las Hojas Son del Viento_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vagabundear",
#         "artist": "Joan Manuel Serrat",
#         "genre": "Pop & International Pop & Latin Music",
#         "album": "Mediterr\u00e1neo",
#         "address": "music/Joan Manuel Serrat - Vagabundear.mp3",
#         "img": "music/Joan Manuel Serrat - Vagabundear_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Demonios",
#         "artist": "Estopa",
#         "genre": "Pop",
#         "album": "X Anniversarivm",
#         "address": "music/09 Estopa - Demonios.mp3",
#         "img": "music/09 Estopa - Demonios_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Partiendo la Pana",
#         "artist": "Estopa",
#         "genre": "null",
#         "album": "Destrangis",
#         "address": "music/Estopa - Partiendo la Pana.mp3",
#         "img": "music/Estopa - Partiendo la Pana_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "El Cuerpo Del Delito (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock & Latin Music",
#         "album": "Nada Personal (Remastered)",
#         "address": "music/Soda Stereo - El Cuerpo Del Delito (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - El Cuerpo Del Delito (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ferm\u00edn (Las Manos De Ferm\u00edn)",
#         "artist": "Almendra",
#         "genre": "null",
#         "album": "30 Anos De Amendra",
#         "address": "music/Almendra - Ferm\u00edn (Las Manos De Ferm\u00edn).mp3",
#         "img": "music/Almendra - Ferm\u00edn (Las Manos De Ferm\u00edn)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Vencidos",
#         "artist": "Joan Manuel Serrat",
#         "genre": "Pop & International Pop & Latin Music",
#         "album": "Mediterr\u00e1neo",
#         "address": "music/Joan Manuel Serrat - Vencidos.mp3",
#         "img": "music/Joan Manuel Serrat - Vencidos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "He Venido",
#         "artist": "Los Zafiros",
#         "genre": "null",
#         "album": "Locura Azul - Original Soundtrack",
#         "address": "music/Locura Azul - Original Soundtrack CD 1 TRACK 5 (320).mp3",
#         "img": "music/Locura Azul - Original Soundtrack CD 1 TRACK 5 (320)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Entre Can\u00edbales (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Canci\u00f3n Animal (Remastered)",
#         "address": "music/Soda Stereo - Entre Can\u00edbales (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Entre Can\u00edbales (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Reflexi\u00f3n",
#         "artist": "X Alfonso",
#         "genre": "Rap/Hip Hop",
#         "album": "Reflexi\u00f3n",
#         "address": "music/X Alfonso - Reflexi\u00f3n.mp3",
#         "img": "music/X Alfonso - Reflexi\u00f3n_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Unravel",
#         "artist": "TK from Ling tosite sigure",
#         "genre": "null",
#         "album": "Unravel",
#         "address": "music/TK from Ling tosite sigure - Unravel.mp3",
#         "img": "music/TK from Ling tosite sigure - Unravel_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Maquiav\u00e9lico",
#         "artist": "Canserbero",
#         "genre": "Rap/Hip Hop & Latin Music",
#         "album": "Muerte",
#         "address": "music/Canserbero - Maquiav\u00e9lico.mp3",
#         "img": "music/Canserbero - Maquiav\u00e9lico_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "WHY AM I STILL IN LA (feat. Shlohmo & D33J)",
#         "artist": "Joji",
#         "genre": "null",
#         "album": "BALLADS 1",
#         "address": "music/Joji - WHY AM I STILL IN LA (feat. Shlohmo   D33J).mp3",
#         "img": "music/Joji - WHY AM I STILL IN LA (feat. Shlohmo   D33J)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Souffle au coeur",
#         "artist": "L'Imp\u00e9ratrice",
#         "genre": "null",
#         "album": "Tako Tsubo",
#         "address": "music/L Imp\u00e9ratrice - Souffle au coeur.mp3",
#         "img": "music/L Imp\u00e9ratrice - Souffle au coeur_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hombre Al Agua (Remasterizado 2007)",
#         "artist": "Soda Stereo",
#         "genre": "Rock",
#         "album": "Canci\u00f3n Animal (Remastered)",
#         "address": "music/Soda Stereo - Hombre Al Agua (Remasterizado 2007).mp3",
#         "img": "music/Soda Stereo - Hombre Al Agua (Remasterizado 2007)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Young Folks (Victoria Bergsman)",
#         "artist": "Peter Bjorn and John, Victoria Bergsman",
#         "genre": "Pop & Rock",
#         "album": "Ich kann Nix Daf\u00fcr",
#         "address": "music/Peter_Bjorn_and_John,_Victoria_Bergsman_Young_Folks_Victoria_Bergsman.mp3",
#         "img": "music/Peter_Bjorn_and_John,_Victoria_Bergsman_Young_Folks_Victoria_Bergsman_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Obertura 777 (Instrumental)",
#         "artist": "La Maquina De Hacer P\u00e1jaros",
#         "genre": "null",
#         "album": "Peliculas",
#         "address": "music/La Maquina De Hacer P\u00e1jaros - Obertura 777 (Instrumental).mp3",
#         "img": "music/La Maquina De Hacer P\u00e1jaros - Obertura 777 (Instrumental)_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Ni oui ni non",
#         "artist": "ZAZ",
#         "genre": "Pop",
#         "album": "Zaz",
#         "address": "music/07 ZAZ - Ni oui ni non.mp3",
#         "img": "music/07 ZAZ - Ni oui ni non_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "No Hay Azul Sin Ti",
#         "artist": "X Alfonso",
#         "genre": "Alternative & Reggae",
#         "album": "No Hay Azul Sin Ti",
#         "address": "music/X Alfonso - No Hay Azul Sin Ti.mp3",
#         "img": "music/X Alfonso - No Hay Azul Sin Ti_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "After Destruction",
#         "artist": "Descartes A Kant",
#         "genre": "null",
#         "album": "After Destruction",
#         "address": "music/Descartes A Kant - After Destruction.mp3",
#         "img": "music/Descartes A Kant - After Destruction_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Hijos",
#         "artist": "X Alfonso",
#         "genre": "null",
#         "album": "Reverse",
#         "address": "music/X Alfonso - Hijos.mp3",
#         "img": "music/X Alfonso - Hijos_cover.jpg"
#     },
#     {
#         "id": 1,
#         "title": "Mil Horas (Album Version)",
#         "artist": "Los Abuelos de la Nada",
#         "genre": "null",
#         "album": "Rock en espa\u00f1ol 80s, 90s y 2000s",
#         "address": "music/Los Abuelos de la Nada - Mil Horas (Album Version).mp3",
#         "img": "music/Los Abuelos de la Nada - Mil Horas (Album Version)_cover.jpg"
#     }
# ]

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

# @app.delete("/songs/{song_id}")
# def delete_song(song_id: int):
#     global songs
#     songs = [song for song in songs if song["id"] != song_id]
#     return {"message": "Song deleted"}

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

# @app.get("/songs/stream/{song_title}")
# def stream_song(song_title: str, request: Request):
#     # Encuentra la URL del archivo de la canción
#     song_url = [s["address"] for s in songs if s["title"] == song_title]
#     if not song_url:
#         raise HTTPException(status_code=404, detail="Song not found")
    
#     file_path = song_url[0]
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="Song file not found")
    
#     file_size = os.path.getsize(file_path)
#     print(str(file_size))
#     range_header = request.headers.get('Range')
#     print(range_header)
#     start = 0
#     end = file_size - 1

#     if range_header:
#         range_match = re.match(r'bytes=(\d+)-(\d+)?', range_header)
#         if range_match:
#             start = int(range_match.group(1))
#             end = int(range_match.group(2)) if range_match.group(2) else end

#     def iterfile():
#         with open(file_path, mode="rb") as file_like:
#             file_like.seek(start)
#             chunk_size = 1024*1024
#             while chunk_size > 0:
#                 chunk = file_like.read(min(8192, chunk_size))
#                 if not chunk:
#                     break
#                 yield chunk
#                 chunk_size -= len(chunk)
    
#     return StreamingResponse(
#         iterfile(),
#         status_code=206,
#         media_type="audio/mp3",
#         headers={
#             'Content-Range': f'bytes {start}-{end}/{file_size}',
#             'Accept-Ranges': 'bytes',
#             # 'Content-Length': str(end - start + 1),
#             'Content-Type': 'audio/mpeg',
#             'X-File-Size': str(file_size)
#         }
        
#     )

@app.get("/songs/stream/{song_title}")
def stream_song(song_title: str, request: Request):

    pass
     # Función iteradora para enviar el contenido real de los chunks
    def iter_chunks():
        # Usamos la función load_chunks_from_json para obtener las direcciones de los chunks
        for chunk_address in load_chunks_from_json("chunks.json", song_title):
            if not os.path.exists(chunk_address):
                raise HTTPException(status_code=404, detail=f"Chunk not found: {chunk_address}")
            
            with open(chunk_address, "rb") as chunk_file:
                # Leemos todo el contenido del chunk y lo enviamos completo
                chunk_data = chunk_file.read()  # Leemos el chunk completo
                yield chunk_data  # Enviamos el chunk completo al frontend

    # Devolvemos los chunks usando StreamingResponse
    return StreamingResponse(
        iter_chunks(),  # Chunks devueltos por la función
        status_code=200,  # Usamos 200 si no manejamos Range directamente
        media_type="audio/mp3",  # O el formato que uses, como audio/mp3
    )
    

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
    chunks = split_audio_file(f"music/{file.filename}") # Create the chunks of the song
    json_data = create_json_chunks(chunks, file.filename) # Save the chunks into a json
    

    img_location = ""
    if image:
        img_location = f"music/{file.filename}_cover.jpg"
        with open(img_location, "wb") as img_file:
            while chunk := await image.read(1024*50):
                img_file.write(chunk)

    new_song = {
        "id": len(songs) + 1,
        "title": title,
        "artist": artist,
        "genre": genre,
        "album": album,
        "address": address,
        "img": img_location
    }
    songs.append(new_song)
    return new_song

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
        
        return [f"{chunks_dir}/chunk_{i + 1}.mp3" for i in range(chunk_count)]
    
    except Exception as e:
        print(f"Error al dividir la canción: {str(e)}")
        return None

def create_json_chunks(chunks, file_path):

    with open('chunks.json', 'r') as file:
        data = json.load(file)
        
    if not file_path in data:
        # Agregar nuevos elementos
        data.setdefault(f"{file_path}", chunks)

        with open('chunks.json', 'w') as file:
            json.dump(data, file, indent=4)

def load_chunks_from_json(json_file, song_title):

    with open(json_file, 'r') as f:
        data = json.load(f)

    for chunk in data[song_title]:
        yield chunk 


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)