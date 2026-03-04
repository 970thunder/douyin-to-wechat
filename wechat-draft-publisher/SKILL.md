---
name: wechat-draft-publisher
description: "公众号草稿发布 - 调用微信 API 发布到草稿箱"
---

# Wechat Draft Publisher

将 HTML 文档发布到公众号草稿箱。

## 工作流程

```
HTML 文档 → 上传图片 → 创建草稿 → 返回草稿 ID
```

## 使用方法

```bash
# 基础用法
wechat-publisher --input article.html --title "文章标题"

# 指定封面图
wechat-publisher --input article.html --cover cover.jpg

# 发布到指定账号
wechat-publisher --input article.html --account main
```

## 配置

### 环境变量

```bash
export WECHAT_APPID="your_appid"
export WECHAT_APPSECRET="your_appsecret"
```

### 多账号配置

```json
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

## API 流程

### 1. 获取 Access Token
```bash
curl "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${APPID}&secret=${APPSECRET}"
```

### 2. 上传图片（如有）
```bash
curl -F media=@cover.jpg "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${TOKEN}&type=image"
```

### 3. 创建草稿
```bash
curl -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${TOKEN}" \
  -d '{
    "articles": [{
      "title": "文章标题",
      "author": "作者",
      "content": "HTML 内容",
      "thumb_media_id": "封面图 ID",
      "digest": "摘要"
    }]
  }'
```

## 输出

```json
{
  "media_id": "xxx",
  "url": "https://mp.weixin.qq.com/s/xxx",
  "status": "draft"
}
```

## 限制

- Access Token 有效期：2 小时
- 草稿箱上限：100 篇
- 图片大小：< 2MB
- 文章字数：< 20000 字

## 错误处理

| 错误码 | 说明 | 处理 |
|--------|------|------|
| 40001 | AppSecret 错误 | 检查配置 |
| 40014 | AccessToken 无效 | 重新获取 |
| 45009 | 草稿箱已满 | 提示清理 |

## 安全建议

- AppSecret 加密存储
- 定期刷新 Access Token
- 限制调用频率（< 1000次/天）

## 完整流程示例

```bash
# 1. 转写视频
douyin-transcriber "https://douyin.com/video/xxx"

# 2. 写作文章
wechat-pm-writer --input summary.md --output article.md

# 3. 排版
wechat-formatter --input article.md --output article.html

# 4. 发布草稿
wechat-publisher --input article.html --title "AI 助手协作系统"
```

## 测试

```bash
# 测试 API 连接
wechat-publisher --test

# 预览草稿（不发布）
wechat-publisher --input article.html --preview
```

---

**版本：** 1.0
**作者：** Alex
**权限要求：** 公众号开发者权限
