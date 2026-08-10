"""关闭不靠谱的 PanWebShare 4K源搜索，保留欧哥、多多、蜡笔"""
import json

with open('jsm.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Keep: 欧哥、多多、蜡笔
# Disable: 快映、木偶、至臻、二小、虎斑、短木
disable_keys = ['快映', '木偶', '至臻', '二小', '虎斑', '短木']

count = 0
for site in data['sites']:
    key = site.get('key', '')
    name = site.get('name', '')
    if key in disable_keys:
        old_s = site.get('searchable', 0)
        old_q = site.get('quickSearch', 0)
        if old_s != 0 or old_q != 0:
            site['searchable'] = 0
            site['quickSearch'] = 0
            count += 1
            print(f'  disabled: {name} (key={key})')
        else:
            print(f'  already off: {name} (key={key})')

print(f'\n关闭 {count} 个 4K 源搜索')

# Count remaining
remaining = [s for s in data['sites'] if s.get('searchable', 0) == 1 or s.get('quickSearch', 0) == 1]
print(f'剩余搜索源: {len(remaining)} 个')

with open('jsm.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('jsm.json 已保存')
