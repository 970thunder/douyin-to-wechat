# 抖音 → 公众号文章生成系统

完整的 AI 协作工具链，将抖音视频转化为精美的公众号文章。

## 🎯 功能

- 📹 **视频转写** - 下载抖音视频，提取音频，Whisper 转文字
- ✍️ **智能写作** - 产品经理/技术专家视角撰写文章
- 🎨 **精美排版** - Markdown 转 HTML，支持多种主题
- 🚀 **一键发布** - 调用微信 API 发布到草稿箱

## 🚀 快速开始

### 1. 安装依赖

```bash
# Python 依赖
pip install openai requests

# 系统依赖
brew install ffmpeg  # macOS
```

### 2. 配置环境变量

```bash
# 必需
export TIKHUB_API_KEY="your_tikhub_key"
export OPENAI_API_KEY="your_openai_key"
export WECHAT_APPID="your_appid"
export WECHAT_APPSECRET="your_appsecret"

# 可选
export UNSPLASH_ACCESS_KEY="your_unsplash_key"  # 配图
```

### 3. 一键执行

```bash
# 完整流程
python scripts/full_workflow.py "https://www.douyin.com/video/xxx" \
  --title "文章标题" \
  --style pm \
  --theme 科技蓝

# Dry run（只生成，不发布）
python scripts/full_workflow.py "URL" --title "标题" --dry-run
```

## 📦 独立使用

### 视频转写

```bash
cd douyin-transcriber
python scripts/transcribe.py "https://www.douyin.com/video/xxx" --output output/
```

**输出：**
- `output/transcript.txt` - 原始转写文本
- `output/summary.md` - 核心总结

### 文章写作

```bash
# 产品经理视角
cd wechat-product-manager-writer
python scripts/writer.py --input ../output/summary.md --output article.md

# 技术专家视角
cd wechat-tech-writer
python scripts/tech_writer.py --input ../output/summary.md --level 进阶
```

### 排版美化

```bash
cd wechat-article-formatter
python scripts/formatter.py --input ../article.md --theme 科技蓝 --output article.html
```

### 发布草稿

```bash
cd wechat-draft-publisher
python scripts/publisher.py --input ../article.html --title "文章标题"
```

## 🎨 主题选择

| 主题 | 颜色 | 适用场景 |
|------|------|----------|
| 科技蓝 | #1890FF | 技术文章、产品介绍 |
| 活力橙 | #FF6B35 | 活动报道、营销内容 |
| 高雅灰 | #333333 | 品牌故事、高端内容 |
| 清新绿 | #52C41A | 生活分享、健康主题 |

## 🎯 免费转写方案

**推荐：Whisper.cpp（完全免费）**

```bash
# 安装（macOS）
brew install whisper-cpp

# 使用
python scripts/transcribe_v2.py "抖音URL" --engine whisper.cpp
```

**成本对比：**
- ❌ OpenAI Whisper：¥0.006/分钟（10分钟 = ¥0.06）
- ✅ Whisper.cpp：**免费**（10分钟 = ¥0）

**节省：100%**

详见：[免费转写方案指南](FREE_TRANSCRIPTION.md)

---

## 📊 成本估算

### 使用免费方案（推荐）
| 步骤 | API | 成本 | 时间 |
|------|-----|------|------|
| 转写 | Tikhub + Whisper.cpp | ¥0.1 | 5-10分钟 |
| 写作 | GPT-4 | ¥0.2-0.5 | 3-5分钟 |
| 排版 | 免费 | ¥0 | 1分钟 |
| 发布 | 微信 API | ¥0 | 1分钟 |
| **总计** | - | **¥0.3-0.6** | **10-17分钟** |

### 使用付费方案
| 步骤 | API | 成本 | 时间 |
|------|-----|------|------|
| 转写 | Tikhub + Whisper | ¥0.5-1.0 | 5-10分钟 |
| 写作 | GPT-4 | ¥0.2-0.5 | 3-5分钟 |
| 排版 | 免费 | ¥0 | 1分钟 |
| 发布 | 微信 API | ¥0 | 1分钟 |
| **总计** | - | **¥0.7-1.5** | **10-17分钟** |

## 📁 项目结构

```
skills/
├── douyin-transcriber/        # 视频转写
│   ├── SKILL.md
│   └── scripts/
│       └── transcribe.py
├── wechat-product-manager-writer/  # PM 写作
│   ├── SKILL.md
│   └── scripts/
│       └── writer.py
├── wechat-tech-writer/        # 技术写作
│   ├── SKILL.md
│   └── scripts/
│       └── tech_writer.py
├── wechat-article-formatter/  # 排版工具
│   ├── SKILL.md
│   └── scripts/
│       └── formatter.py
├── wechat-draft-publisher/    # 发布工具
│   ├── SKILL.md
│   └── scripts/
│       └── publisher.py
├── scripts/
│   └── full_workflow.py       # 完整流程
├── WORKFLOW.md                # 流程说明
└── README.md                  # 本文件
```

## 🔧 高级用法

### 多账号配置

```json
// ~/.wechat/config.json
{
  "accounts": {
    "main": {
      "appid": "wx1234567890",
      "appsecret": "secret123"
    },
    "tech": {
      "appid": "wx0987654321",
      "appsecret": "secret456"
    }
  }
}
```

### 自定义主题

```python
# 添加新主题到 wechat-article-formatter/scripts/formatter.py
self.themes = {
    ...
    "自定义": {
        "primary": "#FF0000",
        "secondary": "#FF6666",
        "text": "#333333",
        "bg": "#FFF0F0"
    }
}
```

### 批量处理

```bash
# 批量转写
for url in $(cat urls.txt); do
  python scripts/full_workflow.py "$url" --title "自动标题" --dry-run
done
```

## ⚠️ 注意事项

1. **版权问题** - 确保视频内容可转载
2. **内容审核** - 发布前人工审核
3. **频率限制** - 公众号每天最多 8 篇
4. **API 限制** - 注意各 API 的调用频率限制

## 🐛 故障排除

### Tikhub 下载失败
```bash
# 检查 API Key
echo $TIKHUB_API_KEY

# 测试连接
curl -H "Authorization: Bearer $TIKHUB_API_KEY" https://api.tikhub.io/v1/user
```

### Whisper 转写失败
```bash
# 检查音频文件
ffprobe output/audio.mp3

# 手动转写
whisper output/audio.mp3 --language zh
```

### 微信 API 错误
```bash
# 测试 Access Token
python scripts/publisher.py --test

# 检查权限
# 确保公众号有开发者权限
```

## 📈 性能优化

- **并发处理** - 多个视频同时转写
- **缓存机制** - 缓存 Access Token
- **队列系统** - 使用 Redis 管理任务队列

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT

---

**作者：** Alex
**版本：** 1.0.0
**更新时间：** 2026-03-03
