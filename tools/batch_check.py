"""
批量检测所有 TVBox 配置文件中的源，关闭失效源的搜索。
只保留确认可用（URL 可达）的源开搜索，其余全部关闭。
"""
import json
import os
import sys
import time
import concurrent.futures
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

TIMEOUT = 10
MAX_WORKERS = 10

def extract_urls_from_ext(ext):
    urls = []
    if isinstance(ext, str):
        parts = ext.split('$$$')
        for part in parts:
            part = part.strip()
            if part.startswith('http://') or part.startswith('https://'):
                urls.append(part)
    elif isinstance(ext, dict):
        for v in ext.values():
            if isinstance(v, str) and (v.startswith('http://') or v.startswith('https://')):
                urls.append(v)
    return urls

def check_url(url):
    start = time.time()
    try:
        parsed = urlparse(url)
        if parsed.hostname in ('127.0.0.1', 'localhost', '::1'):
            return ('skip', 0, 'local')
        req = Request(url, headers={'User-Agent': 'okhttp/3.15', 'Accept': '*/*'})
        with urlopen(req, timeout=TIMEOUT) as resp:
            resp.read(2048)
            latency = int((time.time() - start) * 1000)
            return ('ok', latency, f'HTTP {resp.status}')
    except HTTPError as e:
        return ('fail', 0, f'HTTP {e.code}')
    except Exception as e:
        return ('fail', 0, str(e)[:50])

def check_site(site, base_dir):
    """检测一个源，返回 (status, name, key)"""
    name = site.get('name', '?')
    key = site.get('key', '')
    
    # 提取可检测的远程 URL
    urls = extract_urls_from_ext(site.get('ext', ''))
    
    has_ok = False
    has_fail = False
    
    for url in urls:
        status, latency, info = check_url(url)
        if status == 'ok':
            has_ok = True
        elif status == 'fail':
            has_fail = True
    
    # 检查本地文件
    api = site.get('api', '')
    if api.startswith('./') or api.startswith('../'):
        full_path = os.path.normpath(os.path.join(base_dir, api))
        if not os.path.exists(full_path):
            has_fail = True
    
    ext = site.get('ext', '')
    if isinstance(ext, str):
        parts = ext.split('$$$')
        for part in parts:
            part = part.strip()
            if part.startswith('./') or part.startswith('../'):
                full_path = os.path.normpath(os.path.join(base_dir, part))
                if not os.path.exists(full_path):
                    has_fail = True

    if has_fail and not has_ok:
        return ('fail', name, key)
    elif has_ok:
        return ('ok', name, key)
    else:
        return ('unknown', name, key)

def process_config(config_path):
    """检测一个配置文件并关闭失效源的搜索"""
    base_dir = os.path.dirname(os.path.abspath(config_path))
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.loads(f.read(), strict=False)
    
    sites = config.get('sites', [])
    if not sites:
        return None
    
    # 并发检测
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_site, site, base_dir): i for i, site in enumerate(sites)}
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()
    
    # 统计和处理
    ok_count = 0
    fail_count = 0
    unknown_count = 0
    closed_search = 0
    ok_names = []
    fail_names = []
    
    for i, site in enumerate(sites):
        status, name, key = results[i]
        if status == 'fail':
            fail_count += 1
            fail_names.append(name)
            # 关闭失效源的搜索
            old_s = site.get('searchable', 0)
            old_q = site.get('quickSearch', 0)
            if old_s != 0 or old_q != 0:
                site['searchable'] = 0
                site['quickSearch'] = 0
                closed_search += 1
        elif status == 'ok':
            ok_count += 1
            ok_names.append(name)
        else:
            unknown_count += 1
    
    # 保存
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    # 统计搜索源
    search_on = sum(1 for s in sites if s.get('searchable',0)==1 or s.get('quickSearch',0)==1)
    
    return {
        'file': os.path.basename(config_path),
        'total': len(sites),
        'ok': ok_count,
        'fail': fail_count,
        'unknown': unknown_count,
        'closed_search': closed_search,
        'search_on': search_on,
        'ok_names': ok_names[:5],
        'fail_names': fail_names[:5],
    }

def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 找到所有根目录的 json 配置
    configs = []
    for f in sorted(os.listdir('.')):
        if not f.endswith('.json') or not os.path.isfile(f):
            continue
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                data = json.loads(fh.read(), strict=False)
            if 'sites' in data and len(data['sites']) > 0:
                configs.append(f)
        except:
            pass
    
    # 也检查 cat
    cat_configs = []
    for root, dirs, files in os.walk('cat'):
        for f in files:
            if f.endswith('.json'):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8') as fh:
                        data = json.loads(fh.read(), strict=False)
                    if 'sites' in data and len(data['sites']) > 0:
                        cat_configs.append(path)
                except:
                    pass
    
    all_configs = configs + cat_configs
    print(f'找到 {len(all_configs)} 个配置文件需要检测\n')
    
    results = []
    for config_path in all_configs:
        print(f'检测: {config_path} ...', flush=True)
        result = process_config(config_path)
        if result:
            results.append(result)
            print(f'  源:{result["total"]} | 可用:{result["ok"]} | 失效:{result["fail"]} | 关闭搜索:{result["closed_search"]} | 剩余搜索:{result["search_on"]}')
    
    # 总结
    print('\n' + '=' * 60)
    print('总结:')
    print(f'{"配置文件":<25s} {"总源":<6s} {"可用":<6s} {"失效":<6s} {"关搜索":<8s} {"剩余搜索":<8s}')
    print('-' * 60)
    for r in results:
        print(f'{r["file"]:<25s} {r["total"]:<6d} {r["ok"]:<6d} {r["fail"]:<6d} {r["closed_search"]:<8d} {r["search_on"]:<8d}')
    print('=' * 60)

if __name__ == '__main__':
    main()
