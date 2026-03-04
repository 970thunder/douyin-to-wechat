---
name: wechat-product-manager-writer
description: "产品经理视角的公众号文章写作 - 从资料到成稿"
---

# Wechat Product Manager Writer

以产品经理视角，将资料转化为公众号文章。

## 工作流程

```
输入资料 → 搜索补充 → 构思框架 → 写作成稿 → 配封面图 → 输出 Markdown
```

## 使用方法

```bash
# 从文件
wechat-pm-writer --input summary.md --output article.md

# 从主题
wechat-pm-writer --topic "AI 助手协作系统"

# 指定风格
wechat-pm-writer --input summary.md --style 专业/轻松/干货
```

## 写作框架

### 产品经理视角（默认）

```markdown
# 标题（吸引眼球）

## 背景与痛点
- 为什么重要
- 用户痛点

## 解决方案
- 核心思路
- 实现方法

## 价值与收益
- 用户收益
- 业务价值

## 行动建议
- 下一步做什么
- 注意事项
```

## 技能要求

- **搜索资料**：调用 `multi-search-engine`
- **配封面图**：Unsplash API / AI 生成
- **写作风格**：参考 `human-writing` skill

## 输出格式

```markdown
---
title: 文章标题
author: 产品经理
date: 2026-03-03
cover: https://images.unsplash.com/...
tags: [AI, 产品, 协作]
---

# 文章标题

正文内容...

## 关键要点

1. 要点一
2. 要点二
3. 要点三

---
*作者：Alex*
*转载请注明出处*
```

## 风格选项

| 风格 | 特点 | 适用场景 |
|------|------|----------|
| 专业 | 数据驱动、逻辑严密 | B2B、技术文章 |
| 轻松 | 故事化、口语化 | B2C、品牌传播 |
| 干货 | 实用技巧、可操作 | 教程、指南 |

## 配图规则

- **封面图**：Unsplash 高质量图片
- **配图比例**：每 500 字 1 张
- **图片来源**：优先 Unsplash，其次 AI 生成

## 示例

**输入：** 抖音视频总结
**输出：** 公众号文章（产品经理视角）

---

**版本：** 1.0
**作者：** Alex
