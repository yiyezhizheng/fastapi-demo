from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="路由演示")

# 1.根路由
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 2.路径参数
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

#3.查询参数
@app.get("/products")
async def get_product(name: str, price: int = 0):
    return {"name": name, "price": price}

#4.POST请求体
class UserCreate(BaseModel):
    username: str
    age: int
    email: str | None = None

@app.post("/users")
async def create_user(user: UserCreate):
    return {"user_data": user}
