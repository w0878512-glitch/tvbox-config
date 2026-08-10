import json

with open('jsm.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
for site in data['sites']:
    name = site.get('name', '')
    key = site.get('key', '')
    # Match 聚合• 搜索 and 鬼鬼 • 搜索
    if ('聚合' in name and '搜索' in name) or ('鬼鬼' in name and '搜索' in name):
        old_s = site.get('searchable', 0)
        old_q = site.get('quickSearch', 0)
        print(f'{name} key={key} searchable={old_s} quickSearch={old_q}')
        if old_s != 0 or old_q != 0:
            site['searchable'] = 0
            site['quickSearch'] = 0
            count += 1
            print(f'  -> disabled')

print(f'\n额外关闭 {count} 个')

with open('jsm.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
