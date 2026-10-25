from pydantic import BaseModel,ValidationError
import json

class Config(BaseModel):
    app_name:str
    port:int

if __name__=="__main__":
    try:
        with open("config.json","r",encoding='utf-8') as f:
            data=json.load(f)
            config=Config(**data)
        print(config.port+1)
    except FileNotFoundError:
        print("配置文件不存在")
    except ValidationError as e:
        print(f"配置文件验证错误：{e}")