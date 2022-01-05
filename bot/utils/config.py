from starlette.config import Config

config = Config(".env")

DATABASE_URL: str = config("DATABASE_URL")
TOKEN: str = config("TOKEN")

