# FastAPI RESTful service
## Getting started
Pull and open a project (tested on PyCharm).  
Configure python interpreter/environment (don't forget to activate venv if use it).  
In terminal (venv or without):  
`pip install poetry`  
`poetry install`   – installs all requirements  
`uvicorn main:app` – runs a server, check it on <http://localhost>  
Tests is working only on 

## Extras
### Docker image
[is here](https://hub.docker.com/repository/docker/alexrastorguev/fastapi_tokens).
Please, run the image by command prompt, not Docker Desktop for match ports:  
`docker run -p 80:80 alexrastorguev/fastapi_tokens`
