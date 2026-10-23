def read_csv(file_path):
    result=[]
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            for line in f:
                result.append(line.strip().split(','))
        return result
    except FileNotFoundError:
        print(f'错误：文件 {file_path} 不存在')
    except UnicodeDecodeError:
        print(f'错误：文件 {file_path} 编码格式不支持')
    except Exception as e:
        print(f'错误：读取文件时发生异常：{e}')
    finally:
        print('读取操作结束')
    return None

def csv_stat(file_path):
    data=read_csv(file_path)
    if data is None or len(data)==0:
        print('统计失败：文件读取异常或文件为空')
        return 
    total_rows=len(data)
    empty_counts=0
    for row in data:
        for cell in row:
            if cell.strip()=='':
                empty_counts+=1
    col_counts=len(data[0])
    col_means={}
    for col_index in range(col_counts):
        col_name=data[0][col_index]
        nums=[]
        for row in data[1:]:
            cell=row[col_index].strip()
            try:
                nums.append(float(cell))
            except:
                continue
        if nums:
            col_means[col_name]=sum(nums)/len(nums)
    print(f'总行数：{total_rows}')
    print('数值列均值：')
    for name, avg in col_means.items():
        print(f'  {name}:{avg}')
    print(f'空值总数：{empty_counts}')

