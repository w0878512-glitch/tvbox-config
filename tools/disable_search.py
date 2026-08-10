#!/usr/bin/env python3
"""关闭失效源、短剧源、盘搜源的搜索"""
import json

with open('jsm.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 21 failed sources - disable search
failed_keys = [
    '三秋影视', '华谊', '薯条', '韩圈', '飞飞', '魔方',
    '修罗影视', '咕咕动漫', '小镇影视', '方舟动漫', '果果短剧',
    '枫叶影视', '永乐影视', '漫国动漫', '金牌影视', '面包影视',
    'fyyy', '骚火影视', 'New6v', '七味', '迅雷吧'
]

# Short drama sources - disable search
short_drama_keys = ['七猫短剧', '河马短剧', '围观短剧', '好看短剧', '星芽短剧', '果果短剧']

# Pan-search sources - disable search
pan_search_keys = ['聚合搜索', '盘搜', '米搜', '酷乐', '鬼鬼搜索', '趣盘']

all_disable = set(failed_keys + short_drama_keys + pan_search_keys)

disabled_count = 0
for site in data.get('sites', []):
    key = site.get('key', '')
    name = site.get('name', '')

    matched = False
    for dk in all_disable:
        if dk == key or dk in key or dk in name:
            matched = True
            break

    if matched:
        old_s = site.get('searchable', 0)
        old_q = site.get('quickSearch', 0)
        if old_s != 0 or old_q != 0:
            site['searchable'] = 0
            site['quickSearch'] = 0
            disabled_count += 1
            print(f'  disabled: {name} (key={key})')
        else:
            print(f'  already off: {name} (key={key})')

print(f'\n共关闭 {disabled_count} 个源的搜索')

# Count remaining search sources
remaining = [s for s in data.get('sites', []) if s.get('searchable', 0) == 1 or s.get('quickSearch', 0) == 1]
print(f'剩余搜索源: {len(remaining)} 个')
for s in remaining:
    print(f'  {s["name"]} (key={s["key"]})')

with open('jsm.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('\njsm.json 已保存')
