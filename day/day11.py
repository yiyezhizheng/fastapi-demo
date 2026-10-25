import re
text = "我的手机号是 13812345678，有事联系。"
pattern=re.findall(r'\d{11}',text)
print(pattern)

import json
with open("config.json","r",encoding="utf-8") as f:
    data=json.load(f)
    print(data['port'])
