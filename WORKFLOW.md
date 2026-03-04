# 抖音 → 公众号完整流程

## 📋 总览

将抖音视频转化为精美的公众号文章。

```
抖音视频 → 转写 → 写作 → 排版 → 发布
```

## 🔄 完整流程

### 1️⃣ 视频转写
**Skill：** `douyin-transcriber`

```bash
douyin-transcriber "https://www.douyin.com/video/xxx"
```

**输出：**
- `transcript.txt` - 原始文本
- `summary.md` - 核心总结

### 2️⃣ 文章写作
**选择视角：**

**产品经理视角：**
```bash
wechat-pm-writer --input summary.md --output article.md
```

**技术专家视角：**
```bash
wechat-tech-writer --input summary.md --output article.md
```

**输出：**
- `article.md` - Markdown 文章

### 3️⃣ 排版美化
**Skill：** `wechat-article-formatter`

```bash
wechat-formatter --input article.md --theme 科技蓝
```

**输出：**
- `article.html` - 精美排版

### 4️⃣ 发布草稿
**Skill：** `wechat-draft-publisher`

```bash
wechat-publisher --input article.html --title "文章标题"
```

**输出：**
- 草稿链接
- media_id

## 🎯 使用场景

### 场景 1：产品宣传
```
抖音产品介绍 → PM Writer → 科技蓝主题 → 发布
```

### 场景 2：技术分享
```
技术讲解视频 → Tech Writer → 代码高亮 → 发布
```

### 场景 3：活动回顾
```
活动记录视频 → PM Writer → 活力橙主题 → 发布
```

## 📊 成本估算

| 步骤 | 成本 | 时间 |
|------|------|------|
| 转写 | ¥0.5-1.0 | 5-10分钟 |
| 写作 | ¥0.2-0.5 | 3-5分钟 |
| 排版 | ¥0 | 1分钟 |
| 发布 | ¥0 | 1分钟 |
| **总计** | **¥0.7-1.5** | **10-17分钟** |

## 🔧 配置清单

### 必需
- [ ] Tikhub API Key
- [ ] OpenAI API Key
- [ ] 公众号 AppID + AppSecret

### 可选
- [ ] Unsplash API（配图）
- [ ] AI 图片生成 API

## 🚀 快速开始

```bash
# 1. 配置环境变量
export TIKHUB_API_KEY="xxx"
export OPENAI_API_KEY="xxx"
export WECHAT_APPID="xxx"
export WECHAT_APPSECRET="xxx"

# 2. 一键执行
douyin-transcriber "URL" && \
wechat-pm-writer --input summary.md && \
wechat-formatter --input article.md && \
wechat-publisher --input article.html
```

## 📝 注意事项

1. **版权问题** - 确保视频内容可转载
2. **内容审核** - 发布前人工审核
3. **频率限制** - 公众号每天最多 8 篇
4. **图片上传** - 需手动上传或使用 CDN

## 🎨 主题推荐

| 内容类型 | 推荐主题 | 特点 |
|----------|----------|------|
| 技术文章 | 科技蓝 | 专业、简洁 |
| 产品介绍 | 高雅灰 | 高端、大气 |
| 活动报道 | 活力橙 | 热情、动感 |
| 生活分享 | 清新绿 | 自然、舒适 |

## 📈 效果对比

**传统方式：**
- 时间：2-4 小时
- 人力：2-3 人
- 成本：¥500+

**AI 协作方式：**
- 时间：10-17 分钟
- 人力：1 人监督
- 成本：¥1.5

**效率提升：** 90%+

---

**创建时间：** 2026-03-03
**维护者：** Alex
**版本：** 1.0
