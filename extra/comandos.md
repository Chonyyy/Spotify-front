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

sudo docker run -it --rm --network distribunet --ip 172.20.240.10 -p 8000:8000 -v $(pwd):/app fastapi:1
