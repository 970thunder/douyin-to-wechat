---
name: wechat-article-formatter
description: "公众号文章排版 - Markdown 转精美 HTML"
---

# Wechat Article Formatter

将 Markdown 文档转换为公众号格式的精美 HTML。

## 工作流程

```
Markdown → 选择主题 → 转换 HTML → 添加样式 → 输出成品
```

## 使用方法

```bash
# 基础用法
wechat-formatter --input article.md --output article.html

# 指定主题
wechat-formatter --input article.md --theme 科技蓝

# 预览
wechat-formatter --input article.md --preview
```

## 内置主题

### 1. 科技蓝
- 主色：#1890FF
- 风格：简洁、专业
- 适用：技术、产品

### 2. 活力橙
- 主色：#FF6B35
- 风格：热情、动感
- 适用：营销、活动

### 3. 高雅灰
- 主色：#333333
- 风格：简约、高端
- 适用：品牌、故事

### 4. 清新绿
- 主色：#52C41A
- 风格：自然、舒适
- 适用：生活、健康

## 排版规则

### 字体
- 正文：16px
- 标题：20px（H1）、18px（H2）
- 行高：1.75

### 段落
- 段间距：20px
- 首行缩进：2 字符
- 最大宽度：677px（公众号限制）

### 强调
- **加粗**：#333 + font-weight: bold
- *斜体*：color: #666 + font-style: italic
- `代码`：背景 #f5f5f5 + padding: 2px 6px

### 图片
- 宽度：100%
- 居中对齐
- 圆角：4px

## HTML 模板

```html
<section style="max-width: 677px; margin: 0 auto;">
  <h1 style="font-size: 20px; color: {{primary_color}}; font-weight: bold;">
    标题
  </h1>

  <p style="font-size: 16px; line-height: 1.75; color: #333;">
    正文内容
  </p>

  <blockquote style="border-left: 4px solid {{primary_color}}; padding-left: 16px; color: #666;">
    引用内容
  </blockquote>
</section>
```

## 高级功能

### 1. 自动配图
```bash
# 自动在段落间插入配图
wechat-formatter --input article.md --auto-image
```

### 2. 重点标注
```markdown
> **重点**：这段会被高亮显示
```

### 3. 列表美化
```markdown
- 列表项 1
- 列表项 2
```

## 输出示例

**输入 Markdown：**
```markdown
# AI 助手协作系统

这是正文内容...

## 核心功能

- 功能 1
- 功能 2
```

**输出 HTML：**
（内联样式的精美排版）

## 技术栈

- **Markdown 解析**：markdown-it
- **模板引擎**：Handlebars
- **样式处理**：Juice（内联 CSS）

## 注意事项

- 公众号不支持外部 CSS，必须内联
- 图片需上传到公众号后台或使用 CDN
- 最大宽度：677px

---

**版本：** 1.0
**作者：** Alex
