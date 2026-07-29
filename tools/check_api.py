import json

with open('js.json', 'r', encoding='utf-8') as f:
    js_config = json.loads(f.read(), strict=False)

keys = {'Moli', 'Ppxzy', 'Libvio', 'Qianfan', 'TGYunPanLocal', '新6V', '美剧迷', '蜡笔网盘', '追剧', '音范丝'}

print("源名称                 | api 字段")
print("-" * 60)
for site in js_config.get('sites', []):
    if site.get('key', '') in keys:
        name = site.get('name', '?')
        api = site.get('api', '')
        print(f"  {name:20s} | {api}")
