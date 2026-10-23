class Document:
    def __init__(self,title,content):
        self.title=title
        self.content=content
    def get_word_count(self):
        return len(self.content)
    def print_info(self):
        print(f'标题：{self.title}，内容字数：{self.get_word_count()}')





if __name__=='__main__':
    doc1=Document("Python学习笔记","今天学习了类与对象的基础用法")
    doc1.print_info()
    doc2=Document("CSV工具开发","给CSV读取函数增加了异常处理逻辑")
    doc2.print_info()