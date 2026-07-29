import json, shutil

# 备份
shutil.copy('fty.json', 'fty.json.bak')

# 加载
with open('fty.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read(), strict=False)

# fty.json 确认可用的源 key
ok_keys = {
    '立播',          # 立播┃不卡
    'Bili',         # 哔哔合集┃弹幕
    'Biliych',      # 哔哔演唱会┃弹幕
    'ZPan',         # 盘搜┃四盘
    'JPan',         # 易搜┃四盘
    'MTV',          # 明星MV
    '少儿教育',       # 少儿教育
    '小学课堂',       # 小学课堂
    '初中课堂',       # 初中课堂
    '高中教育',       # 高中课堂
}

# 先收集实际的 key 看看
all_keys = []
for site in config.get('sites', []):
    all_keys.append((site.get('key', ''), site.get('name', '')))

# 处理
changed = 0
kept = []
for site in config.get('sites', []):
    key = site.get('key', '')
    if key in ok_keys:
        site['searchable'] = 1
        site['quickSearch'] = 1
        kept.append(site.get('name', key))
    else:
        old_s = site.get('searchable', 0)
        old_q = site.get('quickSearch', 0)
        if old_s != 0 or old_q != 0:
            changed += 1
        site['searchable'] = 0
        site['quickSearch'] = 0

# 保存
with open('fty.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(f'完成! 关闭了 {changed} 个源的搜索')
print(f'保留搜索的源 ({len(kept)} 个):')
for name in kept:
    print(f'  Y {name}')

if len(kept) == 0:
    print('\n注意: 没匹配到任何 key, 打印所有 key 供参考:')
    for k, n in all_keys:
        print(f'  {k:30s} | {n}')
