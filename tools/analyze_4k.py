import json

data = json.load(open('jsm.json', 'r', encoding='utf-8'))

k4_sources = [s for s in data['sites'] if '4K' in s.get('name', '')]

print(f'4K源共 {len(k4_sources)} 个\n')

# Group by api/ext to find duplicates
api_groups = {}
for s in k4_sources:
    api = s.get('api', '')
    ext = s.get('ext', '')
    jar = s.get('jar', '')
    # The key differentiator is usually the ext (config URL) or api
    if isinstance(ext, dict):
        group_key = json.dumps(ext, sort_keys=True)
    else:
        group_key = ext if ext else api
    if group_key not in api_groups:
        api_groups[group_key] = []
    api_groups[group_key].append(s)

print('=== 按 ext/api 分组 ===\n')
for key, sources in sorted(api_groups.items(), key=lambda x: -len(x[1])):
    if len(sources) > 1:
        print(f'[重复组] 共 {len(sources)} 个指向同一配置:')
        print(f'  ext/api: {key[:80]}...' if len(key) > 80 else f'  ext/api: {key}')
        for s in sources:
            print(f'    - {s["name"]} (key={s["key"]})')
        print()

print('\n=== 详细信息 ===\n')
for s in k4_sources:
    print(f'{s["name"]} (key={s["key"]})')
    print(f'  type={s.get("type","")} api={s.get("api","")[:60]}')
    ext_val = s.get("ext", "")
    if isinstance(ext_val, dict):
        ext_val = json.dumps(ext_val)
    print(f'  ext={str(ext_val)[:80]}')
    print(f'  jar={s.get("jar","")[:80]}')
    print()
