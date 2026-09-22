# 人工智能与媒体计算团队 · 实验室主页

纯静态站点（HTML + CSS + 原生 JavaScript），无需构建步骤，可直接部署到 GitHub Pages。

## 目录结构

```
lab-site/
├── index.html            # 首页：简介 / 研究方向概览 / 最新动态 / 加入我们
├── research.html         # 研究方向 / 科研项目 / 研究成果
├── people.html           # 团队成员（教师、在读学生招募说明）
├── news.html             # 新闻动态（全部）
├── join.html             # 加入我们（硕博研究生、本科生科研与竞赛）
├── assets/
│   ├── css/style.css     # 全站样式
│   ├── js/main.js        # 移动端导航、导航高亮、新闻渲染、入场动画
│   ├── js/news.js        # ★ 新闻动态数据源，日常维护主要改这里
│   ├── image/            # 人员照片原始图（**.gitignored**，含个人邮箱的 xlsx 也被忽略）
│   └── img/
│       ├── people/       # 网页实际使用的压缩照片（由 tools/ 生成）
│       └── favicon.svg
├── tools/
│   └── build-people-images.py   # 照片批量压缩脚本
└── README.md
```

## 本地预览

```bash
cd lab-site
python -m http.server 8000
# 浏览器打开 http://localhost:8000
```

Windows 下若 `python` 不可用，可用 `npx serve` 或直接双击 `index.html`（本地相对路径可正常显示）。

## 部署到 GitHub Pages

1. 在 GitHub 新建仓库，推荐命名为 `aimc-heu.github.io`（`aimc-heu` 换成你的用户名或组织名），这样访问地址就是 `https://aimc-heu.github.io`。
2. 把本目录内容推送到仓库默认分支（`main`）：

   ```bash
   git init
   git add .          # .gitignore 会自动跳过原始照片与人员收集表
   git commit -m "init: lab homepage"
   git branch -M main
   git remote add origin https://github.com/<用户名>/<仓库名>.github.io.git
   git push -u origin main
   ```

> **隐私说明**：仓库内不包含学生邮箱和原始照片。原始资料（`assets/image/`、`实验室人员收集.xlsx`）
> 仅保存在本地，`.gitignore` 已排除。如果将来把仓库公开，请确认这两处未通过其它渠道泄露。

3. 仓库 → **Settings → Pages** → Build and deployment → Source 选 `Deploy from a branch` → Branch 选 `main` / `/(root)` → Save。
4. 等待约 1 分钟，访问 `https://<用户名>.github.io` 即可。

> 若仓库名不是 `<用户名>.github.io`（例如叫 `lab-site`），访问地址会是
> `https://<用户名>.github.io/lab-site/`。本站点全部使用相对路径，子目录部署无需改动。
>
> 绑定自定义域名：在仓库根目录放一个 `CNAME` 文件，内容为域名（如 `aimc.cs.hrbeu.edu.cn`），
> 并在域名服务商处添加一条指向 `<用户名>.github.io` 的 CNAME 解析。
>
> 使用 GitHub Actions 部署（可选）：仓库根目录加空文件 `.nojekyll` 可跳过 Jekyll 处理。

## 日常维护

| 想改什么 | 改哪里 |
| --- | --- |
| 新增 / 修改新闻动态 | `assets/js/news.js`（数组，最新的放最前面），首页自动显示最新 5 条 |
| 修改研究方向内容 | `research.html` 中对应的 `<div class="card">` 区块 |
| 增删团队成员 | `people.html` 中对应的 `.members` 网格，复制一张 `.member` 卡片改姓名 / 层次 / 邮箱 / 主页 |
| 新增成员照片 | 原图放 `assets/image/`（中文名）→ 在 `tools/build-people-images.py` 的 `NAME_MAP` 加一行 → 跑脚本 → 网页引用 `assets/img/people/<拼音>.jpg` |
| 修改项目 / 论文 / 专利 | `research.html` 中 `.list` 与 `.bullets` 区块 |
| 换主题色 | `assets/css/style.css` 顶部 `:root` 里的 `--accent` / `--accent-2` |
| 改导航菜单 | 每个 HTML 文件顶部的 `.nav-links`（4 个文件保持一致） |

## 照片处理

原始照片体积很大（单张最大 39 MB，合计 54 MB），直接放上网会严重拖慢加载。
`tools/build-people-images.py` 负责把它们压成网页版：

```bash
pip install Pillow
cd lab-site
python tools/build-people-images.py
```

- 输入 `assets/image/`（原图不动，仅存档）、输出 `assets/img/people/*.jpg`
- 长边 640px、JPEG 质量 82、自动修正手机拍摄方向、透明通道合成白底
- 实测 54.1 MB → 0.5 MB（单张 12–65 KB）
- 输出用 ASCII 文件名（拼音），避免中文路径在部分静态托管上的编码问题
- 新增成员时在脚本的 `NAME_MAP` 里补一行即可

## 后续可增补的内容

初版刻意不展示任何未经确认的信息。以下内容确认后可以随时加回（加在哪一栏见表）：

- [ ] 团队联系邮箱、办公地址 → 四个页面页脚的「联系方式」栏，直接加 `<p>邮箱：xxx@hrbeu.edu.cn</p>`
- [ ] 往届学生姓名与毕业去向 → `people.html` 可新增一节（结构同「在读学生」）
- [ ] 获奖与荣誉、学术与社会兼职 → 已删除，原始内容仍可在本仓库的 Git 历史或源 Markdown 中找回
- [ ] 近五年代表性论文列表（标题 / 期刊 / 年份 / DOI / 代码仓库） → `research.html`「学术论文」卡片
- [ ] 团队 logo（可替换 `assets/img/favicon.svg` 与导航中的 `.mark`）

## 设计说明

- 浅色主题、单一强调色（HEU 蓝 `#17458f`）、大留白，学术风格。
- 响应式：桌面三栏 / 平板两栏 / 手机单栏，导航在窄屏折叠为汉堡菜单。
- 无第三方依赖、无字体外链，国内访问不受 CDN 影响。
- 尊重 `prefers-reduced-motion`，关闭动画偏好时自动停用入场效果。
