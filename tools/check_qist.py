from urllib.request import urlopen, Request
import json

# 搜索 qist 用户
url = 'https://api.github.com/users/qist'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
        print('qist 用户存在')
        print(f'  公开仓库数: {data.get("public_repos", 0)}')
        print(f'  最后活跃: {data.get("updated_at", "")}')
except Exception as e:
    print(f'qist 用户状态: {e}')

# 搜索 qist 的仓库
print()
url2 = 'https://api.github.com/users/qist/repos?sort=updated&per_page=15'
req2 = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urlopen(req2, timeout=10) as resp:
        repos = json.loads(resp.read())
        print(f'qist 的仓库 ({len(repos)} 个):')
        for r in repos:
            name = r['name']
            pushed = r.get('pushed_at', '')[:10]
            stars = r.get('stargazers_count', 0)
            desc = (r.get('description') or '')[:50]
            print(f'  {name:30s} Stars:{stars:3d} | {pushed} | {desc}')
except Exception as e:
    print(f'获取仓库列表失败: {e}')
