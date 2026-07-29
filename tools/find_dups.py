import os, hashlib

def file_hash(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

# 比较 xiaosa/js/ vs js/
print('=== xiaosa/js/ vs js/ 重复文件 ===')
dup_js = []
if os.path.isdir('xiaosa/js') and os.path.isdir('js'):
    for name in sorted(os.listdir('xiaosa/js')):
        root_file = os.path.join('js', name)
        xiao_file = os.path.join('xiaosa/js', name)
        if os.path.isfile(root_file) and os.path.isfile(xiao_file):
            if file_hash(root_file) == file_hash(xiao_file):
                dup_js.append((name, os.path.getsize(xiao_file)))

total = sum(s for _, s in dup_js)
print(f'  完全相同: {len(dup_js)} 个, 共 {total/1024:.0f} KB')
for name, size in dup_js[:10]:
    print(f'    {name}')
if len(dup_js) > 10:
    print(f'    ... 等共 {len(dup_js)} 个')

# 比较 xiaosa/py/ vs py/
print('\n=== xiaosa/py/ vs py/ 重复文件 ===')
dup_py = []
if os.path.isdir('xiaosa/py') and os.path.isdir('py'):
    for name in sorted(os.listdir('xiaosa/py')):
        root_file = os.path.join('py', name)
        xiao_file = os.path.join('xiaosa/py', name)
        if os.path.isfile(root_file) and os.path.isfile(xiao_file):
            if file_hash(root_file) == file_hash(xiao_file):
                dup_py.append((name, os.path.getsize(xiao_file)))

total2 = sum(s for _, s in dup_py)
print(f'  完全相同: {len(dup_py)} 个, 共 {total2/1024:.0f} KB')
for name, size in dup_py:
    print(f'    {name}')

# 比较 jar
print('\n=== jar 重复 ===')
if os.path.isfile('xiaosa/spider.jar') and os.path.isfile('jar/spider.jar'):
    h1 = file_hash('xiaosa/spider.jar')
    h2 = file_hash('jar/spider.jar')
    size_mb = os.path.getsize('xiaosa/spider.jar') / 1024 / 1024
    if h1 == h2:
        print(f'  xiaosa/spider.jar == jar/spider.jar (重复, {size_mb:.1f} MB)')
    else:
        print(f'  xiaosa/spider.jar != jar/spider.jar (不同版本)')

# 比较 xiaosa/json/ vs json/
print('\n=== xiaosa/json/ vs json/ 重复文件 ===')
dup_json = []
if os.path.isdir('xiaosa/json') and os.path.isdir('json'):
    for name in sorted(os.listdir('xiaosa/json')):
        root_file = os.path.join('json', name)
        xiao_file = os.path.join('xiaosa/json', name)
        if os.path.isfile(root_file) and os.path.isfile(xiao_file):
            if file_hash(root_file) == file_hash(xiao_file):
                dup_json.append((name, os.path.getsize(xiao_file)))

total3 = sum(s for _, s in dup_json)
print(f'  完全相同: {len(dup_json)} 个, 共 {total3/1024:.0f} KB')
for name, size in dup_json:
    print(f'    {name}')

# 总结
print(f'\n=== 总结 ===')
grand_total = total + total2 + total3
if os.path.isfile('xiaosa/spider.jar') and os.path.isfile('jar/spider.jar'):
    if file_hash('xiaosa/spider.jar') == file_hash('jar/spider.jar'):
        grand_total += os.path.getsize('xiaosa/spider.jar')
print(f'  总共可节省: {grand_total/1024/1024:.1f} MB')
