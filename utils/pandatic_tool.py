import json
from pydantic import BaseModel, ValidationError

class Settings(BaseModel):
    encoding: str
    default_file: str
    enable_stat: bool

class AppConfig(BaseModel):
    app_name: str
    version: str
    settings: Settings

try:
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    config = AppConfig(**data)
    print(config.app_name, config.settings.default_file)
except ValidationError as e:
    print(f"配置文件验证失败：{e}")
except FileNotFoundError:
    print("错误：配置文件不存在")
