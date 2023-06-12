# FastAPI RESTful service
## Getting started
Pull and open a project (tested on PyCharm).  
Configure python interpreter/environment (don't forget to activate venv if use it).  
In terminal (venv or without):  
`pip install poetry` or `python -m pip install poetry`  
`poetry install`   – installs all requirements  
`uvicorn main:app` – runs a server, check it on <http://localhost>  
That's all! Now you can use HTTP for requesting. Also, there is test_user_client.py, a small example of work.

Tests is working only on empty (just launched) server, because they are sensitive to certain data.

## Extras
### Docker image
[is here](https://hub.docker.com/repository/docker/alexrastorguev/fastapi_tokens).
Please, run the image by command prompt, not Docker Desktop for match ports:  
`docker run -p 80:80 alexrastorguev/fastapi_tokens`
