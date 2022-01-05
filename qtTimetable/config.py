from starlette import config
from starlette.config import Config

config = Config(".env")

DATABASE: str = config("DATABASE")
USER: str = config("USER")
PASSWORD: str = config("PASSWORD")