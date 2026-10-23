import json
config = {
    "app_name": "csv_tool",
    "version": "1.0.0",
    "settings": {
        "encoding": "utf-8",
        "default_file": "test.csv",
        "enable_stat": True
    }
}
with open("config.json",'w',encoding='utf-8') as f:
    json.dump(config,f,ensure_ascii=False,indent=2)
with open("config.json",'r',encoding='utf-8') as f:
    data=json.load(f)
    print(data['app_name'],data['settings']['default_file'])
config['version']='1.0.1'
with open("config.json",'w',encoding='utf-8') as f:
    json.dump(config,f,ensure_ascii=False,indent=2)
