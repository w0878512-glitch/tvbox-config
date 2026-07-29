import json, shutil

# 备份
shutil.copy('jsm.json', 'jsm.json.bak')

# 加载
with open('jsm.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read(), strict=False)

# 确认可用的 15 个源的 key
ok_keys = {
    '双星99',
    '天堂',
    '橘汁',
    '热播影视',
    '王子',
    '苹果',
    '茉莉',
    '蓝鹰',
    '薯条',
    '高清',
    '修罗影视',
    '农民影视',
    '剧圈99',
    '厂长影视',
    '曼波动漫',
}

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
with open('jsm.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(f'完成! 关闭了 {changed} 个源的搜索')
print(f'保留搜索的源 ({len(kept)} 个):')
for name in kept:
    print(f'  ✅ {name}')
