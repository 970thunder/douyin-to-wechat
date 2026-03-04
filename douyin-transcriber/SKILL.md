---
name: douyin-transcriber
description: "抖音视频转写工具 - 下载视频、提取音频、Whisper 转文字、生成总结"
---

# Douyin Transcriber

将抖音视频转写成文字，并生成核心总结。

## 工作流程

```
抖音 URL → Tikhub 下载 → ffmpeg 提取音频 → Whisper 转写 → LLM 总结 → 输出文档
```

## 前置要求

- Tikhub API Key（环境变量：`TIKHUB_API_KEY`）
- OpenAI API Key（Whisper + GPT-4）
- ffmpeg 已安装

## 使用方法

```bash
# 基础用法
douyin-transcriber "https://www.douyin.com/video/..."

# 输出到指定目录
douyin-transcriber "URL" --output ./output/

# 只转写，不总结
douyin-transcriber "URL" --no-summary
```

## 输出文件

```
output/
├── video.mp4          # 原视频
├── audio.mp3          # 提取的音频
├── transcript.txt     # 原始转写文本
└── summary.md         # 核心总结文档
```

## 技术栈

- **视频下载**：Tikhub API
- **音频提取**：ffmpeg
- **转写**：OpenAI Whisper API / whisper.cpp
- **总结**：GPT-4 / GLM-4

## 配置

### 环境变量

```bash
export TIKHUB_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
```

### Whisper 选项

```json
{
  "whisper": {
    "model": "whisper-1",  // 或 "whisper-large-v3"
    "language": "zh",
    "temperature": 0
  }
}
```

## 示例输出

**summary.md：**
```markdown
# 视频标题

**时长：** 3分28秒
**作者：** @用户名
**发布时间：** 2026-03-03

## 核心观点

1. 观点一
2. 观点二
3. 观点三

## 关键内容

### 第一部分
转写内容...

### 第二部分
转写内容...

## 金句摘录

- "金句1"
- "金句2"
```

## 错误处理

| 错误 | 处理 |
|------|------|
| Tikhub 限流 | 等待 60 秒重试 |
| Whisper 超时 | 降级到 whisper-tiny |
| 视频不可用 | 提示用户提供新链接 |

## 成本估算

- Tikhub：¥0.1/视频
- Whisper：¥0.006/分钟
- GPT-4：¥0.03/1K tokens

**总计：** 约 ¥0.5-1.0/视频

---

**版本：** 1.0
**作者：** Alex
