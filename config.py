import os, sys
import json
from pydantic import BaseModel, Field


def get_home():
    if sys.platform == "win32":
        home_path = os.environ["USERPROFILE"]
    elif sys.platform in ["linux", "darwin"]:
        home_path = os.environ["HOME"]
    else:
        home_path = os.getcwd()
    return home_path

class Config(BaseModel):
    download_path: str = Field(get_home())
    cookie: str = Field("")

    def __init__(self):
        data = self.read_config()
        super().__init__(**data)

    def read_config(self):
        with open("config.json", "r", encoding="utf8") as f:
            content = f.read()
        return json.loads(content) if content else {}

    def update_config(self):
        with open("config.json", "w", encoding="utf8") as f:
            f.write(json.dumps(self.dict(), indent=4))


config = Config()
