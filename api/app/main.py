from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger

from .routers import account, divert, transfer


description="""
### SecureBank API - progetto SD
"""

app = FastAPI(
    title="securebank",
    description=description,
    version="0.0.1",
    contact={
      "name": "Alberto Ventafridda",
      "url": "https://halb.it"
    },
)

# During development, the webserver runs on a separate origin
# therefore a CORS configuration on the api server is required.
# In production (both k8s and docker-compose) the api server will be behind the same
# reverse-proxy serving the static website, so there won't be any CORS issue
origins = [
    "http://halb.local",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account.router)
app.include_router(divert.router)
app.include_router(transfer.router)

