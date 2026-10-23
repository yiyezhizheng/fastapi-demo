from pathlib import Path

for file in Path('.').rglob('*.txt'):
    new_name=file.with_stem(f'new_{file.stem}')
    file.rename(new_name)