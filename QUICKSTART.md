# 快速开始指南

5 分钟快速上手抖音 → 公众号文章生成系统。

## 📋 准备工作

### 1. 获取 API Keys

**Tikhub API**（视频下载）
- 访问：https://tikhub.io
- 注册并获取 API Key
- 费用：¥0.1/视频

**OpenAI API**（转写 + 写作）
- 访问：https://platform.openai.com
- 创建 API Key
- 费用：Whisper ¥0.006/分钟，GPT-4 ¥0.03/1K tokens

**微信公众号**（发布）
- 登录：https://mp.weixin.qq.com
- 开发 → 基本配置 → 获取 AppID 和 AppSecret
- 要求：已认证的服务号

### 2. 安装系统依赖

```bash
# macOS
brew install python3 ffmpeg

# Ubuntu
sudo apt install python3 python3-pip ffmpeg
```

### 3. 安装 Python 依赖

```bash
cd skills/
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制示例文件
cp .env.example .env

# 编辑配置
nano .env

# 加载环境变量
source .env
```

## 🚀 第一次运行

### 测试配置

```bash
python scripts/test_workflow.py
```

预期输出：
```
✅ 依赖检查通过
✅ API Keys 配置正确
✅ ffmpeg 已安装
✅ 脚本文件完整
✅ API 连接正常
```

### 完整流程

```bash
# 找一个抖音视频 URL
URL="https://www.douyin.com/video/7345678901234567890"

# 一键执行（dry run 模式）
python scripts/full_workflow.py "$URL" \
  --title "测试文章" \
  --style pm \
  --theme 科技蓝 \
  --dry-run

# 查看输出
ls -la output/
```

### 正式发布

```bash
# 去掉 --dry-run 参数
python scripts/full_workflow.py "$URL" \
  --title "我的第一篇文章" \
  --style pm \
  --theme 科技蓝
```

## 📝 实际案例

### 案例 1：产品介绍视频

```bash
URL="https://www.douyin.com/video/xxx"

python scripts/full_workflow.py "$URL" \
  --title "AI 助手如何提升工作效率" \
  --style pm \
  --theme 科技蓝
```

**预期结果：**
- 转写：5 分钟
- 写作：3 分钟
- 排版：1 分钟
- 发布：1 分钟
- **总计：10 分钟，成本 ¥1.2**

### 案例 2：技术教程视频

```bash
URL="https://www.douyin.com/video/yyy"

python scripts/full_workflow.py "$URL" \
  --title "FastAPI 性能优化实战" \
  --style tech \
  --theme 高雅灰
```

**预期结果：**
- 包含代码示例
- 性能对比数据
- 架构图（Mermaid）
- **总计：12 分钟，成本 ¥1.5**

## ⚙️ 自定义配置

### 修改写作风格

编辑 `wechat-product-manager-writer/scripts/writer.py`:

```python
style_prompts = {
    "专业": "使用数据驱动、逻辑严密的写作风格...",
    "轻松": "使用故事化、口语化的写作风格...",
    "干货": "使用实用技巧、可操作的写作风格...",
    "自定义": "你的自定义风格..."  # 添加新风格
}
```

### 添加新主题

编辑 `wechat-article-formatter/scripts/formatter.py`:

```python
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

## 🐛 常见问题

### Q1: Tikhub 下载失败？

```bash
# 检查 API Key
curl -H "Authorization: Bearer $TIKHUB_API_KEY" \
  https://api.tikhub.io/v1/user

# 检查余额
# 访问 https://tikhub.io/dashboard
```

### Q2: Whisper 转写速度慢？

```bash
# 使用本地 Whisper（更快）
pip install whisper-cpp

# 修改配置
export WHISPER_MODEL=whisper-tiny  # 更快但质量略低
```

### Q3: 微信发布失败？

```bash
# 检查权限
# 确保公众号有"素材管理"和"草稿箱"权限

# 测试连接
python scripts/publisher.py --test
```

### Q4: 成本太高？

```bash
# 使用 GPT-3.5-turbo（便宜 10 倍）
export GPT_MODEL=gpt-3.5-turbo

# 使用本地 Whisper
export WHISPER_MODEL=local

# 只转写，不写作
python douyin-transcriber/scripts/transcribe.py "$URL" --no-summary
```

## 📈 进阶技巧

### 批量处理

```bash
# 创建 URL 列表
cat > urls.txt << EOF
https://www.douyin.com/video/111
https://www.douyin.com/video/222
https://www.douyin.com/video/333
EOF

# 批量处理
while read url; do
  python scripts/full_workflow.py "$url" --title "自动标题" --dry-run
done < urls.txt
```

### 定时任务

```bash
# 每天早上 9 点执行
crontab -e

# 添加
0 9 * * * cd /path/to/skills && python scripts/scheduled_task.py
```

### Webhook 集成

```python
# 接收飞书/钉钉通知
import requests

def notify_completion(result):
    webhook_url = "https://open.feishu.cn/..."
    requests.post(webhook_url, json={
        "msg_type": "text",
        "content": {"text": f"文章已生成: {result['url']}"}
    })
```

## 📚 下一步

- [ ] 阅读完整文档：[README.md](README.md)
- [ ] 了解工作流程：[WORKFLOW.md](WORKFLOW.md)
- [ ] 自定义配置：编辑 `.env` 文件
- [ ] 添加新功能：参考 SKILL.md 编写新技能

## 💬 获取帮助

- **文档**：查看各个 skill 的 SKILL.md
- **示例**：查看 `examples/` 目录
- **问题**：提交 Issue

---

**祝你使用愉快！🎉**
