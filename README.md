# TVBox 配置仓库

基于 [qist/tvbox](https://github.com/qist/tvbox) 同步维护，定期检测源可用性并关闭失效源的搜索。

## 配置地址

在 TVBox / OK影视 / 猫影视 中填入以下地址即可使用：

| 配置 | 说明 | 地址 |
|------|------|------|
| **jsm.json (推荐)** | js.json + 0826 合集，家庭电视可用 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/jsm.json` |
| js.json | Panda Groove go包 + 道长drpy(js) + YouTube | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/js.json` |
| dianshi.json | 与 jsm 相同生态，spider.jar | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/dianshi.json` |
| fty.json | 飞兔影视，教育/直播/哔哩为主 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/fty.json` |
| 0821.json | 大而全，饭太硬基础上添加优质源 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/0821.json` |
| 0825.json | 小而精，Panda Groove go包 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/0825.json` |
| 0826.json | 饭太硬 jar 和配置 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/0826.json` |
| 0827.json | fongmi jar 和配置 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/0827.json` |
| 9918.json | pg.jar 生态 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/9918.json` |
| 99188.json | pg23a94bb.jar 生态 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/99188.json` |
| XYQ.json | 香雅情 jar 和配置 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/XYQ.json` |
| cat (影猫) | 纯js，配合猫影视使用 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/cat/tjs/tv_config.json` |
| xiaosa (潇洒) | 潇洒接口 | `https://gh.ddlc.top/https://raw.githubusercontent.com/w0878512-glitch/tvbox-config/main/xiaosa/api.json` |

> 备用加速前缀（替换 `https://gh.ddlc.top/`）：
> - `https://mirror.ghproxy.com/`
> - `https://github.moeyy.xyz/`
> - `https://gh-proxy.com/`

## 配置与 jar 包对应关系

| 配置文件 | spider (jar包) |
|---------|---------------|
| jsm.json / dianshi.json | spider.jar |
| js.json / 0825.json / 9918.json | pg.jar |
| 99188.json | pg23a94bb.jar |
| fty.json / 0821.json / 0826.json | fan.txt |
| 0827.json | custom_spider.jar |
| XYQ.json | XYQ.jar |
| cat | 无需 jar，纯 js |
| xiaosa | xiaosa/spider.jar |

> ⚠️ 不同配置使用不同 jar 包，不可混用。

## 目录结构

```
├── jsm.json / js.json / fty.json 等   ← 各套主配置
├── jar/                               ← 插件包 (spider)
├── xiaosa/                            ← 潇洒生态资源
├── js/                                ← drpy js 爬虫脚本
├── py/                                ← python 爬虫脚本
├── json/                              ← 源数据配置
├── lib/                               ← 公共 js 依赖库
├── FTY/                               ← 飞兔生态资源
├── cat/                               ← 影猫 (CatVod) 生态
├── live/                              ← IPTV 直播源
└── tools/                             ← 工具脚本
    ├── check_sites.py                 ←   单个配置源检测
    ├── batch_check.py                 ←   批量检测所有配置
    └── tvbox.py                       ←   配置加密/解密
```

## 工具使用

### 检测单个配置的源可用性
```bash
cd tools
python -X utf8 check_sites.py ../jsm.json --output report.txt
```

### 批量检测所有配置并关闭失效源搜索
```bash
python -X utf8 tools/batch_check.py
```

### 加密/解密配置
```bash
python tools/tvbox.py input.json output.json enc   # 加密
python tools/tvbox.py input.json output.json dec   # 解密
```

## APP 推荐

| APP | 地址 | 特点 |
|-----|------|------|
| OK影视 (FongMi) | [GitHub](https://github.com/FongMi/Release) | 支持直播多线路、自动换源、投屏 |
| takagen99版 | [GitHub](https://github.com/takagen99/Box) | 支持直播回放，界面美观 |
| 猫影视 (CatVod) | [GitHub](https://github.com/catvod/CatVodOpen) | 界面简洁，多平台 |
| 手机竖屏版 | [GitHub](https://github.com/XiaoRanLiu3119/TVBoxOS-Mobile) | 手机适配 |

## 免责声明

所有资源均来自网络，仅供学习研究使用，请于 24 小时内删除。如有侵权请联系删除。
