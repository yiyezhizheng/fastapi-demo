import math

def calculate_area(lenth:float,width:float)->float:
    return lenth*width

def greet(name:str="Guest")->None:
    print(f'Hello,{name}')

def get_stats(nums:list[int])->tuple[int,int]:
    maxnum=max(nums)
    minnum=min(nums)
    return maxnum,minnum

def read_csv_safely(file_path:str)->bool:
    try:
        with open(file_path,"r",encoding="utf-8") as f:
            return True
    except Exception as e:
        print(f"文件读取失败,原因:{e}")
        return False

if __name__=="__main__":
    a=calculate_area(5, 3)
    print(a)
    greet()
    greet("Alice")
    nums = [10, 5, 8, 20]
    max_val,min_val=get_stats(nums)
    print(max_val,min_val)
    read_csv_safely(r"D:\project\github\MyStudy\ai-dev-learning\fastapi-demo\test.csv")


