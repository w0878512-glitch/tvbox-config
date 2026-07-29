from urllib.request import urlopen, Request
import json

queries = [
    'tvbox+config+pushed:>2026-06-01',
    'tvbox+spider+pushed:>2026-06-01',
    'drpy+tvbox',
    'catvod+open+pushed:>2026-06-01',
    'xiaosa+tvbox',
]

print('搜索活跃的 TVBox 相关仓库...\n')
seen = set()
results = []

for q in queries:
    try:
        url = f'https://api.github.com/search/repositories?q={q}&sort=updated&order=desc&per_page=10'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            for item in data.get('items', []):
                full_name = item['full_name']
                if full_name in seen:
                    continue
                seen.add(full_name)
                results.append({
                    'name': full_name,
                    'stars': item.get('stargazers_count', 0),
                    'pushed': item.get('pushed_at', ''),
                    'desc': (item.get('description') or '')[:60],
                    'url': item.get('html_url', ''),
                })
    except Exception as e:
        print(f'  搜索 [{q}] 失败: {e}')

# 按最后更新排序
results.sort(key=lambda x: x['pushed'], reverse=True)

print(f'找到 {len(results)} 个相关仓库:\n')
for r in results[:25]:
    pushed_date = r['pushed'][:10]
    name = r['name']
    stars = r['stars']
    desc = r['desc']
    url = r['url']
    print(f'  {name}')
    print(f'    Stars: {stars} | 最后更新: {pushed_date}')
    print(f'    {desc}')
    print(f'    {url}')
    print()
