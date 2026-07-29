import json

# 加载两个配置
with open('js.json', 'r', encoding='utf-8') as f:
    js_config = json.loads(f.read(), strict=False)
with open('jsm.json', 'r', encoding='utf-8') as f:
    jsm_config = json.loads(f.read(), strict=False)

# js.json 确认可用的 10 个 key
js_ok_keys = {
    'Moli', 'Ppxzy', 'Libvio', 'Qianfan',
    'TGYunPanLocal', '新6V', '美剧迷', '蜡笔网盘', '追剧', '音范丝'
}

# jsm.json 已有的所有 key
jsm_keys = {s.get('key', '') for s in jsm_config.get('sites', [])}

# 找出 js.json 可用但 jsm.json 里没有的
missing = []
for site in js_config.get('sites', []):
    key = site.get('key', '')
    if key in js_ok_keys and key not in jsm_keys:
        missing.append(site)

print(f'js.json 确认可用: {len(js_ok_keys)} 个')
print(f'jsm.json 已有源: {len(jsm_keys)} 个')
print(f'jsm.json 缺少的可用源: {len(missing)} 个')
print()
if missing:
    for s in missing:
        name = s.get('name', '?')
        key = s.get('key', '?')
        print(f'  {name} (key: {key})')
else:
    print('  无，jsm.json 已经包含了所有 js.json 中确认可用的源')
