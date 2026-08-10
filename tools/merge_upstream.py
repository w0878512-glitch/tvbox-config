"""合并上游新增源到 jsm.json，删除上游删除的源（保留蓝鹰），更新api/ext变化的源"""
import json
import subprocess

# Load local and upstream
with open('jsm.json', 'r', encoding='utf-8') as f:
    local = json.load(f)

r = subprocess.run(['git', 'show', 'upstream/master:jsm.json'], capture_output=True)
upstream = json.loads(r.stdout.decode('utf-8'))

local_keys = {s['key'] for s in local['sites']}
upstream_keys = {s['key'] for s in upstream['sites']}

# 1. Add 12 new sources (with searchable=0, quickSearch=0)
new_keys = upstream_keys - local_keys
added = []
for us in upstream['sites']:
    if us['key'] in new_keys:
        us['searchable'] = 0
        us['quickSearch'] = 0
        local['sites'].append(us)
        added.append(us.get('name', us['key']))

print(f'新增 {len(added)} 个源（搜索关闭）:')
for name in added:
    print(f'  + {name}')

# 2. Delete sources that upstream removed (except 蓝鹰)
keep_keys = {'蓝鹰'}  # Keep this one
remove_keys = (local_keys - upstream_keys) - keep_keys
removed = []
local['sites'] = [s for s in local['sites'] if s['key'] not in remove_keys or s['key'] in keep_keys]
for key in remove_keys:
    removed.append(key)

print(f'\n删除 {len(removed)} 个源（上游已删除）:')
for key in removed:
    print(f'  - {key}')
print('  (保留: 蓝鹰)')

# 3. Update api/ext for changed sources
updated = []
for us in upstream['sites']:
    key = us['key']
    if key in local_keys and key not in new_keys:
        for i, ls in enumerate(local['sites']):
            if ls['key'] == key:
                if us.get('api') != ls.get('api') or str(us.get('ext', '')) != str(ls.get('ext', '')):
                    # Update api and ext, keep local searchable/quickSearch settings
                    old_searchable = ls.get('searchable', 0)
                    old_quickSearch = ls.get('quickSearch', 0)
                    # Copy upstream site but preserve search settings
                    us_copy = us.copy()
                    us_copy['searchable'] = old_searchable
                    us_copy['quickSearch'] = old_quickSearch
                    local['sites'][i] = us_copy
                    updated.append(us.get('name', key))
                break

print(f'\n更新 {len(updated)} 个源的 api/ext:')
for name in updated:
    print(f'  ~ {name}')

# Save
with open('jsm.json', 'w', encoding='utf-8') as f:
    json.dump(local, f, ensure_ascii=False, indent=2)

# Final count
remaining_search = [s for s in local['sites'] if s.get('searchable', 0) == 1 or s.get('quickSearch', 0) == 1]
print(f'\n总源数: {len(local["sites"])}')
print(f'搜索源数: {len(remaining_search)}（不变）')
print('\njsm.json 已保存')
