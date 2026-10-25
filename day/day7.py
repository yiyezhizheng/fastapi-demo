import csv

def analyze_csv(file_path):
    # 你的代码写在这里
    try:
        rows_count=0
        empty_count=0
        with open(file_path,"r",newline="",encoding="utf-8") as f:
          reader=csv.reader(f)
          for row in reader:
             rows_count+=1
             for cell in row:
                if cell=="":
                   empty_count+=1
        print(f'总行数：{rows_count},空值数：{empty_count}')
    except Exception as e:
       print(f'发生错误，原因：{e}')
