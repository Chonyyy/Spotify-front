# Comandos

## Para montar el front

``` python

python -m http.server 8080

```

## Para inicia el servidor web

``` python

uvicorn app:app --reload --host 0.0.0.0 --port 8000

```

## Docker

### Montar el contenedor

sudo docker run -it --rm --name fastapi_container -p 8000:8001 -v $(pwd):/app fastapi:1
