from pathlib import Path

for file in Path('.').rglob('*.txt'):
    new_name=file.with_stem(f'new_{file.stem}')
    file.rename(new_name)





for file in Path("目标文件夹").rglob("[1-3].jpg"):
    new_name=file.with_stem(f'pic_{file.stem}')
    file.rename(new_name)