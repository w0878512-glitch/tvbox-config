# TVBox 配置仓库

自用 TVBox 多源配置，包含 4 套生态，选一套填入电视即可。

## 配置地址

将以下地址填入 TVBox / CatVod 的"配置地址"即可使用：

| 生态 | 配置地址 | 特点 |
|------|---------|------|
| **xiaosa (推荐)** | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/jsm.json` | APP逆向为主，源稳定 |
| pg (胖哥) | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/js.json` | 网站爬虫为主，源多 |
| fty (飞兔) | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/fty.json` | 教育/直播/哔哩为主 |
| cat (影猫) | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/cat/tjs/tv_config.json` | 纯js，不需要jar |

> 备用加速前缀：将 `https://gh.ddlc.top/` 替换为 `https://mirror.ghproxy.com/` 或 `https://github.moeyy.xyz/`

## 目录结构

```
├── jsm.json / js.json / fty.json   ← 三套主配置
├── jar/                            ← 插件包
│   ├── spider.jar                  ←   jsm.json 使用
│   ├── pg.jar                      ←   js.json 使用
│   └── fan.txt                     ←   fty.json 使用
├── xiaosa/                         ← xiaosa 生态资源 (py/json/js)
├── js/                             ← pg 生态的 js 爬虫脚本
├── py/                             ← python 爬虫脚本
├── json/                           ← 源数据配置
├── lib/                            ← 公共 js 依赖库 (drpy引擎等)
├── FTY/                            ← fty 生态资源
├── cat/                            ← 影猫 (CatVod) 生态
├── live/                           ← IPTV 直播源 (按地区)
├── tools/                          ← 工具脚本
│   ├── check_sites.py              ←   源可用性检测
│   ├── compare_configs.py          ←   配置对比
│   └── tvbox.py                    ←   配置加密/解密
└── archive/                        ← 历史快照 (不再使用)
```

## 工具使用

### 检测源是否可用

```bash
cd tools
python -X utf8 check_sites.py ../jsm.json --output report.txt
```

会生成报告，标记出 ✅可用 / ❌失效 / 📁本地依赖 的源。

### 加密/解密配置

```bash
python tools/tvbox.py input.json output.json enc   # 加密
python tools/tvbox.py input.json output.json dec   # 解密
```

## 注意事项

- 不同配置使用不同的 jar 包，不可混用
- 源失效是常态，定期运行检测脚本清理
- 搜索结果杂乱时，减少 `searchable` 为 1 的源数量
