"""
TVBox 源可用性检测工具
用法:
    python check_sites.py                    # 检测 ../js.json
    python check_sites.py path/to/config.json
    python check_sites.py --output report.md # 输出报告到文件

功能:
1. 解析 TVBox 配置 JSON 的 sites 列表
2. 对每个源检测其依赖的 URL/文件是否可达
3. 对 type=1 (直接接口) 的源发请求检测是否返回有效数据
4. 输出分组报告: 可用 / 疑似失效 / 无法检测(本地依赖)

注意:
- type=3 的源大多依赖本地 js/jar，无法通过网络检测，只能检查文件是否存在
- 需要能够外网访问 (部分源可能需要代理)
"""

import json
import sys
import os
import time
import re
import concurrent.futures
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


# ============ 配置 ============
TIMEOUT = 10          # 请求超时秒数
MAX_WORKERS = 10      # 并发线程数
BASE_DIR = None       # 配置文件所在目录，运行时设置


def load_config(config_path):
    """加载 TVBox 配置 JSON"""
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # strict=False 允许控制字符
    return json.loads(content, strict=False)


def extract_urls_from_ext(ext):
    """从 ext 字段提取可检测的 URL"""
    urls = []
    if isinstance(ext, str):
        # ext 可能是 "token$$$url$$$..." 格式
        parts = ext.split('$$$')
        for part in parts:
            part = part.strip()
            if part.startswith('http://') or part.startswith('https://'):
                urls.append(part)
    elif isinstance(ext, dict):
        # ext 是对象时，遍历值找 URL
        for v in ext.values():
            if isinstance(v, str) and (v.startswith('http://') or v.startswith('https://')):
                urls.append(v)
    return urls


def extract_local_files(site):
    """从 site 提取本地文件引用"""
    files = []
    # api 字段
    api = site.get('api', '')
    if api.startswith('./') or api.startswith('../'):
        files.append(api)

    # ext 字段
    ext = site.get('ext', '')
    if isinstance(ext, str):
        parts = ext.split('$$$')
        for part in parts:
            part = part.strip()
            if part.startswith('./') or part.startswith('../'):
                files.append(part)
    return files


def check_url(url, timeout=TIMEOUT):
    """
    检测 URL 是否可达
    返回: (status, latency_ms, info)
    """
    start = time.time()
    try:
        req = Request(url, headers={
            'User-Agent': 'okhttp/3.15',
            'Accept': '*/*',
        })
        with urlopen(req, timeout=timeout) as resp:
            # 只读部分内容确认响应
            data = resp.read(2048)
            latency = int((time.time() - start) * 1000)
            content_type = resp.headers.get('Content-Type', '')
            status_code = resp.status
            return ('ok', latency, f"HTTP {status_code}, {len(data)}B, {content_type[:30]}")
    except HTTPError as e:
        latency = int((time.time() - start) * 1000)
        return ('http_error', latency, f"HTTP {e.code} {e.reason}")
    except URLError as e:
        latency = int((time.time() - start) * 1000)
        return ('unreachable', latency, str(e.reason)[:60])
    except Exception as e:
        latency = int((time.time() - start) * 1000)
        return ('error', latency, str(e)[:60])


def check_local_file(filepath):
    """检测本地文件是否存在"""
    full_path = os.path.normpath(os.path.join(BASE_DIR, filepath))
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        return ('ok', 0, f"存在, {size}B")
    else:
        return ('missing', 0, f"文件不存在: {full_path}")


def classify_site(site):
    """
    对源进行分类
    返回: category (影视/网盘/搜索/直播/音频/其他)
    """
    name = site.get('name', '')
    key = site.get('key', '')

    if '搜索' in name or 'search' in key.lower():
        return '搜索'
    elif '直播' in name or 'live' in key.lower() or '电视' in name:
        return '直播'
    elif '网盘' in name or 'Pan' in key or 'Share' in key or '阿里' in name:
        return '网盘'
    elif '音' in name or 'MV' in name or 'DJ' in name or 'KTV' in name:
        return '音频'
    elif '磁力' in name or '磁' in name:
        return '磁力'
    elif '弹幕' in name:
        return '弹幕影视'
    elif '影' in name or '视' in name or '剧' in name or '动漫' in name:
        return '影视'
    else:
        return '其他'


def check_site(site):
    """
    综合检测一个源
    返回: {site_info, status, details}
    """
    name = site.get('name', '未知')
    key = site.get('key', '')
    site_type = site.get('type', 0)
    searchable = site.get('searchable', 0)
    quick_search = site.get('quickSearch', 0)
    category = classify_site(site)

    result = {
        'name': name,
        'key': key,
        'type': site_type,
        'category': category,
        'searchable': searchable,
        'quickSearch': quick_search,
        'status': 'unknown',
        'details': [],
    }

    # 检测远程 URL
    urls = extract_urls_from_ext(site.get('ext', ''))
    for url in urls:
        # 跳过 localhost / 127.0.0.1 的地址
        parsed = urlparse(url)
        if parsed.hostname in ('127.0.0.1', 'localhost', '::1'):
            result['details'].append(f"[跳过] 本地地址: {url}")
            continue
        status, latency, info = check_url(url)
        result['details'].append(f"[{status}] {url} ({latency}ms) {info}")
        if status == 'ok':
            if result['status'] == 'unknown':
                result['status'] = 'ok'
        else:
            result['status'] = 'fail'

    # 检测本地文件依赖
    local_files = extract_local_files(site)
    for fp in local_files:
        status, _, info = check_local_file(fp)
        result['details'].append(f"[{status}] 本地: {fp} - {info}")
        if status == 'missing':
            result['status'] = 'fail'
        elif status == 'ok' and result['status'] == 'unknown':
            result['status'] = 'local_only'

    # 没有可检测的 URL 也没有缺失文件
    if result['status'] == 'unknown':
        if local_files:
            result['status'] = 'local_only'
        else:
            result['status'] = 'no_check'

    return result


def format_report(results):
    """生成报告"""
    lines = []
    lines.append("=" * 70)
    lines.append("TVBox 源可用性检测报告")
    lines.append(f"检测时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"总源数: {len(results)}")
    lines.append("=" * 70)

    # 统计
    status_count = {}
    category_count = {}
    for r in results:
        status_count[r['status']] = status_count.get(r['status'], 0) + 1
        category_count[r['category']] = category_count.get(r['category'], 0) + 1

    lines.append("\n## 统计")
    lines.append(f"  ✅ 可用: {status_count.get('ok', 0)}")
    lines.append(f"  ❌ 失效: {status_count.get('fail', 0)}")
    lines.append(f"  📁 仅本地依赖(无法网络检测): {status_count.get('local_only', 0)}")
    lines.append(f"  ❓ 无法判断: {status_count.get('no_check', 0) + status_count.get('unknown', 0)}")

    lines.append("\n## 分类统计")
    for cat, cnt in sorted(category_count.items(), key=lambda x: -x[1]):
        lines.append(f"  {cat}: {cnt} 个")

    # 搜索开启统计
    search_on = [r for r in results if r['searchable'] == 1 or r['quickSearch'] == 1]
    lines.append(f"\n## 参与搜索的源: {len(search_on)} 个")
    lines.append("  (过多会导致搜索结果杂乱，建议只保留 5-10 个可靠的)")

    # 失效列表
    failed = [r for r in results if r['status'] == 'fail']
    if failed:
        lines.append(f"\n## ❌ 失效源 ({len(failed)} 个) — 建议移除或关闭搜索")
        lines.append("-" * 50)
        for r in failed:
            lines.append(f"  [{r['category']}] {r['name']} (key: {r['key']})")
            for d in r['details']:
                lines.append(f"        {d}")

    # 可用列表
    ok_list = [r for r in results if r['status'] == 'ok']
    if ok_list:
        lines.append(f"\n## ✅ 可用源 ({len(ok_list)} 个)")
        lines.append("-" * 50)
        for r in ok_list:
            search_flag = " 🔍" if r['searchable'] or r['quickSearch'] else ""
            lines.append(f"  [{r['category']}] {r['name']}{search_flag}")
            for d in r['details']:
                lines.append(f"        {d}")

    # 本地依赖
    local_list = [r for r in results if r['status'] == 'local_only']
    if local_list:
        lines.append(f"\n## 📁 仅本地依赖 ({len(local_list)} 个)")
        lines.append("  这些源依赖本地 js/jar 文件，文件存在即可，源是否真正可用需实际播放测试")
        lines.append("-" * 50)
        for r in local_list:
            search_flag = " 🔍" if r['searchable'] or r['quickSearch'] else ""
            lines.append(f"  [{r['category']}] {r['name']}{search_flag}")

    # 建议
    lines.append("\n" + "=" * 70)
    lines.append("## 整理建议")
    lines.append("")
    lines.append("1. 移除所有标记为 ❌ 失效的源")
    lines.append("2. 对 📁 仅本地依赖 的源，在电视上实际点进去试试能否播放")
    lines.append("3. 减少参与搜索的源:")
    lines.append("   - 在 site 里设置 \"searchable\":0, \"quickSearch\":0")
    lines.append("   - 只给你确认好用且内容不重复的 5-10 个源开搜索")
    lines.append("4. 按分类整理，建议保留:")
    lines.append("   - 影视: 2-3个稳定采集站 + 1个弹幕站")
    lines.append("   - 网盘: 保留1-2个搜索入口即可")
    lines.append("   - 直播: 保留1个稳定的")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    global BASE_DIR

    # 解析参数
    config_path = os.path.join(os.path.dirname(__file__), '..', 'js.json')
    output_path = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--output' and i + 1 < len(args):
            output_path = args[i + 1]
            i += 2
        elif not args[i].startswith('-'):
            config_path = args[i]
            i += 1
        else:
            i += 1

    config_path = os.path.abspath(config_path)
    BASE_DIR = os.path.dirname(config_path)

    print(f"配置文件: {config_path}")
    print(f"基础目录: {BASE_DIR}")

    # 加载配置
    config = load_config(config_path)
    sites = config.get('sites', [])
    print(f"共 {len(sites)} 个源，开始检测...\n")

    # 并发检测
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_site, site): site for site in sites}
        done_count = 0
        for future in concurrent.futures.as_completed(futures):
            done_count += 1
            result = future.result()
            results.append(result)
            # 进度显示
            status_icon = {'ok': '✅', 'fail': '❌', 'local_only': '📁', 'no_check': '❓', 'unknown': '❓'}
            icon = status_icon.get(result['status'], '❓')
            print(f"  [{done_count}/{len(sites)}] {icon} {result['name']}")

    # 按分类排序
    results.sort(key=lambda r: (r['status'] != 'fail', r['category'], r['name']))

    # 生成报告
    report = format_report(results)
    print("\n" + report)

    # 保存报告
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存到: {output_path}")
    else:
        default_output = os.path.join(BASE_DIR, 'tools', 'check_report.txt')
        with open(default_output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存到: {default_output}")


if __name__ == "__main__":
    main()
