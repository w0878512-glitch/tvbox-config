"""测试 9 个 csp_PanWebShare 4K 源的站点可达性和响应速度"""
import json
import urllib.request
import urllib.error
import time
import ssl

data = json.load(open('jsm.json', 'r', encoding='utf-8'))

# Find all PanWebShare sources
pan_sources = [s for s in data['sites'] if s.get('api', '') == 'csp_PanWebShare']

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print(f'csp_PanWebShare 源共 {len(pan_sources)} 个\n')
print(f'{"源名":<12} {"站点数":<6} {"可达":<6} {"最快响应":<10} {"首选站点"}')
print('-' * 80)

results = []

for s in pan_sources:
    name = s['name']
    ext = s.get('ext', {})
    sites = ext.get('site', []) if isinstance(ext, dict) else []
    
    reachable = 0
    fastest_time = 99999
    fastest_site = ''
    
    for site_url in sites[:3]:  # Test first 3 sites max
        try:
            start = time.time()
            req = urllib.request.Request(site_url, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0')
            resp = urllib.request.urlopen(req, timeout=5, context=ctx)
            elapsed = (time.time() - start) * 1000
            reachable += 1
            if elapsed < fastest_time:
                fastest_time = elapsed
                fastest_site = site_url
        except Exception as e:
            pass
    
    fastest_str = f'{fastest_time:.0f}ms' if fastest_time < 99999 else 'N/A'
    results.append((name, len(sites), reachable, fastest_time, fastest_site))
    print(f'{name:<12} {len(sites):<6} {reachable:<6} {fastest_str:<10} {fastest_site[:50]}')

print('\n=== 排名（按可达性 + 速度） ===\n')
# Sort by reachable (desc) then fastest time (asc)
results.sort(key=lambda x: (-x[2], x[3]))
for i, (name, total, reach, speed, site) in enumerate(results, 1):
    speed_str = f'{speed:.0f}ms' if speed < 99999 else 'N/A'
    status = '✅' if reach > 0 else '❌'
    print(f'  {i}. {status} {name:<12} 可达{reach}/{total}站 最快{speed_str}')
