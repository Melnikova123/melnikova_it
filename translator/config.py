from starlette.config import Config


config = Config(".env")


key: str = config("KEY")
endpoint: str = config("ENDPOINT")
location: str = config("LOCATION")
