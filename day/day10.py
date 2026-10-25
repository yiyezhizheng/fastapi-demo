class Dog:
    def __init__(self,name:str,age:int):
        self.name=name
        self.age=age

    def bark(self)->None:
        print(f"{self.name} 在汪汪叫！")



class Document:
    def __init__(self,title:str,context:str):
        self.title=title
        self.context=context


    def __str__(self)->str:
        return f"文档标题：[{self.title}]，内容：[{self.context}]"







if __name__=="__main__":
    dog=Dog("旺财",3)
    dog.bark()

    doc=Document("Python基础", "Python是一种编程语言")
    print(doc)