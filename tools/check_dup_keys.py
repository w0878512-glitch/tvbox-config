import json, os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

for f in sorted(os.listdir('.')):
    if not f.endswith('.json') or not os.path.isfile(f):
        continue
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.loads(fh.read(), strict=False)
        sites = data.get('sites', [])
        if not sites:
            continue
        keys = {}
        for s in sites:
            k = s.get('key', '')
            if k:
                if k not in keys:
                    keys[k] = []
                keys[k].append(s.get('name', '?'))
        dups = {k: v for k, v in keys.items() if len(v) > 1}
        if dups:
            print(f'{f}: {len(dups)} 组重复 key')
            for k, names in dups.items():
                print(f'    key="{k}" x{len(names)}: {names}')
        else:
            print(f'{f}: 无重复 key ({len(sites)} sites)')
    except Exception as e:
        print(f'{f}: 解析失败 {e}')
