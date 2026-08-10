"""对比本地 jsm.json 和上游的差异"""
import json
import subprocess

local = json.load(open('jsm.json', 'r', encoding='utf-8'))
r = subprocess.run(['git', 'show', 'upstream/master:jsm.json'], capture_output=True)
upstream = json.loads(r.stdout.decode('utf-8'))

local_keys = {s['key'] for s in local['sites']}
upstream_keys = {s['key'] for s in upstream['sites']}

new_keys = upstream_keys - local_keys
removed_keys = local_keys - upstream_keys

print(f'上游新增源: {len(new_keys)} 个')
for k in sorted(new_keys):
    s = next(x for x in upstream['sites'] if x['key'] == k)
    print(f'  + {s.get("name", "?")} (key={k})')

print(f'\n上游已删除(你本地还有): {len(removed_keys)} 个')
for k in sorted(removed_keys):
    s = next(x for x in local['sites'] if x['key'] == k)
    print(f'  - {s.get("name", "?")} (key={k})')

# Check for sites that exist in both but have different api/ext
print(f'\n共同源中 api/ext 有变化的:')
count = 0
for us in upstream['sites']:
    key = us['key']
    if key in local_keys:
        ls = next(x for x in local['sites'] if x['key'] == key)
        if us.get('api') != ls.get('api') or str(us.get('ext','')) != str(ls.get('ext','')):
            count += 1
            if count <= 10:
                print(f'  ~ {us.get("name", "?")} (key={key}) api/ext 变了')
if count > 10:
    print(f'  ... 还有 {count-10} 个')
print(f'  共 {count} 个')
