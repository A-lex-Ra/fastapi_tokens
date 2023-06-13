# FastAPI RESTful service
## Getting started
Pull and open a project (tested on PyCharm).  
Configure python interpreter/environment (don't forget to activate venv if use it).  
In terminal (venv or without):  
`pip install poetry` or `python -m pip install poetry`  
`poetry install`   – installs all requirements  
`uvicorn main:app` – runs a server, check it on <http://localhost>  

That's all! Now you can use HTTP for requesting.  
There is two URIs (excluding root): GET /secret_token and GET /employee_info  
Also, there is [simple shell client](test_user_client.py), a small example of work.

## Extras
### Tests
Tests is working only on empty (just launched) server, because they are sensitive to certain data.
### Docker image [is here](https://hub.docker.com/repository/docker/alexrastorguev/fastapi_tokens)  
Publish inner port 80 in run:  
`docker run -p 80:80 alexrastorguev/fastapi_tokens` or  
`docker run -p  127.0.0.1:8000:80 alexrastorguev/fastapi_tokens` to specify ip and port
