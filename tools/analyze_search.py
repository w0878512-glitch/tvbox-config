import json

data = json.load(open('jsm.json', 'r', encoding='utf-8'))
remaining = [s for s in data['sites'] if s.get('searchable', 0) == 1 or s.get('quickSearch', 0) == 1]
print(f'剩余搜索源: {len(remaining)} 个\n')

app_sources = [s for s in remaining if 'APP' in s.get('name', '')]
k4_sources = [s for s in remaining if '4K' in s.get('name', '')]
caiji_sources = [s for s in remaining if s.get('type', 0) == 1]
other = [s for s in remaining if s not in app_sources and s not in k4_sources and s not in caiji_sources]

print(f'=== APP源 ({len(app_sources)}个) ===')
for s in app_sources:
    print(f'  {s["name"]} (key={s["key"]})')

print(f'\n=== 4K源 ({len(k4_sources)}个) ===')
for s in k4_sources:
    print(f'  {s["name"]} (key={s["key"]})')

print(f'\n=== 采集站 type=1 ({len(caiji_sources)}个) ===')
for s in caiji_sources:
    print(f'  {s["name"]} (key={s["key"]})')

print(f'\n=== 其他 ({len(other)}个) ===')
for s in other:
    print(f'  {s["name"]} (key={s["key"]}) type={s.get("type", "?")}')
