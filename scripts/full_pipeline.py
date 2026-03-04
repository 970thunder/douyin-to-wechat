#!/usr/bin/env python3
"""
抖音 → 公众号完整自动化流程
一键执行：转写 → 搜索资料 → 构思框架 → 写作 → 排版 → HTML输出
"""

import os
import sys
import subprocess
from pathlib import Path
import argparse
import json
import requests

class DouyinToWechatPipeline:
    def __init__(self, output_dir: Path = Path("output")):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # API Keys
        self.tikhub_api_key = os.getenv("TIKHUB_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # 脚本路径
        self.skills_dir = Path(__file__).parent.parent

    def log(self, message: str, emoji: str = "📌"):
        """打印日志"""
        print(f"\n{emoji} {message}")
        print("=" * 60)

    def step1_transcribe(self, url: str) -> Path:
        """步骤 1: 视频转写"""
        self.log("步骤 1/6: 视频转写", "📹")

        transcribe_script = self.skills_dir / "douyin-transcriber" / "scripts" / "transcribe_v2.py"
        
        cmd = [
            "python3", str(transcribe_script),
            url,
            "--engine", "whisper.cpp",
            "--output", str(self.output_dir)
        ]
        
        env = os.environ.copy()
        env["TIKHUB_API_KEY"] = self.tikhub_api_key
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"转写失败: {result.stderr}")
        
        transcript_path = self.output_dir / "transcript.txt"
        print(f"✅ 转写完成: {transcript_path}")
        
        return transcript_path

    def step2_search(self, transcript_path: Path) -> Path:
        """步骤 2: 使用 Tavily 搜索相关资料"""
        self.log("步骤 2/6: 搜索相关资料", "🔍")

        # 读取转写文本
        transcript = transcript_path.read_text(encoding="utf-8")
        
        # 提取关键词（取前200字作为查询）
        keywords = transcript[:200].replace("\n", " ")
        
        # 使用 Tavily API 搜索
        search_results = []
        
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if tavily_api_key:
            try:
                response = requests.post(
                    "https://api.tavily.com/search",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {tavily_api_key}"
                    },
                    json={
                        "query": keywords,
                        "search_depth": "basic",
                        "max_results": 5
                    },
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get("results", []):
                        search_results.append({
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "content": item.get("content", "")[:300]  # 限制长度
                        })
                    print(f"✅ Tavily 搜索成功")
                else:
                    print(f"⚠️ Tavily 搜索失败: {response.status_code}")
            except Exception as e:
                print(f"⚠️ 搜索出错: {e}")
        else:
            print("⚠️ 未设置 TAVILY_API_KEY，跳过搜索")
        
        # 保存搜索结果
        search_path = self.output_dir / "search_results.json"
        search_path.write_text(json.dumps(search_results, ensure_ascii=False, indent=2), encoding="utf-8")
        
        print(f"✅ 找到 {len(search_results)} 条相关资料")
        return search_path

    def step3_outline(self, transcript_path: Path, search_path: Path) -> Path:
        """步骤 3: 构思文章框架"""
        self.log("步骤 3/6: 构思文章框架", "💡")

        # 读取内容
        transcript = transcript_path.read_text(encoding="utf-8")
        
        search_results = []
        if search_path.exists():
            search_data = json.loads(search_path.read_text(encoding="utf-8"))
            search_results = search_data
        
        # 使用 DeepSeek/OpenAI 生成大纲
        from openai import OpenAI
        
        # 支持自定义 API base URL（DeepSeek）
        base_url = os.getenv("OPENAI_BASE_URL")
        client = OpenAI(api_key=self.openai_api_key, base_url=base_url)
        
        prompt = f"""你是一位资深的内容创作者，请基于以下视频转写内容和相关资料，构思一篇公众号文章的框架。

视频转写内容：
{transcript[:1000]}

相关资料：
{json.dumps(search_results[:3], ensure_ascii=False, indent=2)}

请输出文章框架，包括：
1. 吸引人的标题（3个备选）
2. 文章结构（5-7个章节）
3. 每个章节的核心观点
4. 建议的配图位置

输出格式：
# 标题选项
1. ...
2. ...
3. ...

# 文章结构
## 第一章：标题
- 核心观点：...
- 建议配图：...

## 第二章：标题
- 核心观点：...
- 建议配图：...
..."""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位经验丰富的公众号内容策划师"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        outline = response.choices[0].message.content
        
        # 保存大纲
        outline_path = self.output_dir / "outline.md"
        outline_path.write_text(outline, encoding="utf-8")
        
        print(f"✅ 文章框架已生成")
        return outline_path

    def step4_write(self, transcript_path: Path, outline_path: Path, style: str = "pm") -> Path:
        """步骤 4: 生成完整文章"""
        self.log("步骤 4/6: 生成完整文章", "✍️")

        # 读取内容
        transcript = transcript_path.read_text(encoding="utf-8")
        outline = outline_path.read_text(encoding="utf-8")
        
        from openai import OpenAI
        
        # 支持自定义 API base URL（DeepSeek）
        base_url = os.getenv("OPENAI_BASE_URL")
        client = OpenAI(api_key=self.openai_api_key, base_url=base_url)
        
        style_prompts = {
            "pm": "产品经理视角：数据驱动、逻辑严密、强调价值和收益",
            "tech": "技术专家视角：深度解析、技术细节、实战经验",
            "casual": "轻松口语：故事化、接地气、易理解"
        }
        
        prompt = f"""你是一位资深的公众号作者，请基于以下内容撰写一篇高质量的文章。

视频转写内容：
{transcript}

文章框架：
{outline}

写作要求：
1. {style_prompts.get(style, style_prompts['pm'])}
2. 严格遵循框架结构
3. 每段不超过150字
4. 使用通俗易懂的语言
5. 添加适当的过渡句
6. 包含实际案例或数据
7. 结尾给出明确的行动建议

请输出完整的 Markdown 格式文章："""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位资深的公众号内容创作者"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )
        
        article = response.choices[0].message.content
        
        # 添加元信息
        article_with_meta = f"""---
title: 公众号文章
date: {self._get_current_date()}
tags: [抖音, 内容创作]
---

{article}"""
        
        # 保存文章
        article_path = self.output_dir / "article.md"
        article_path.write_text(article_with_meta, encoding="utf-8")
        
        print(f"✅ 文章已生成 ({len(article)} 字)")
        return article_path

    def step5_format(self, article_path: Path, theme: str = "科技蓝") -> Path:
        """步骤 5: 格式化为公众号 HTML"""
        self.log("步骤 5/6: 格式化为公众号 HTML", "🎨")

        # 读取文章
        article = article_path.read_text(encoding="utf-8")
        
        # 使用 DeepSeek/OpenAI 生成精美的 HTML
        from openai import OpenAI
        
        # 支持自定义 API base URL（DeepSeek）
        base_url = os.getenv("OPENAI_BASE_URL")
        client = OpenAI(api_key=self.openai_api_key, base_url=base_url)
        
        prompt = f"""你是一位前端开发专家，请将以下 Markdown 文章转换为适合微信公众号的精美 HTML 格式。

文章内容：
{article}

要求：
1. 使用内联 CSS 样式（公众号不支持外部样式表）
2. 配色方案：{theme}（科技蓝用 #1E88E5，活力橙用 #FF6F00，高雅灰用 #546E7A）
3. 字体大小：标题 18px，正文 16px，引用 14px
4. 行间距：1.8
5. 段落间距：20px
6. 添加适当的装饰元素（分割线、引用样式）
7. 图片占位符使用：https://via.placeholder.com/800x400?text=图片描述
8. 适配移动端阅读

请输出完整的 HTML 代码（只需要 body 内容，不需要 html/head 标签）："""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位精通微信公众号排版的前端工程师"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        html_content = response.choices[0].message.content
        
        # 提取 HTML（去掉 markdown 代码块标记）
        if "```html" in html_content:
            html_content = html_content.split("```html")[1].split("```")[0].strip()
        elif "```" in html_content:
            html_content = html_content.split("```")[1].split("```")[0].strip()
        
        # 保存 HTML
        html_path = self.output_dir / "article.html"
        html_path.write_text(html_content, encoding="utf-8")
        
        print(f"✅ HTML 已生成")
        return html_path

    def step6_preview(self, html_path: Path) -> None:
        """步骤 6: 生成本地预览"""
        self.log("步骤 6/6: 生成本地预览", "👀")

        # 创建完整的 HTML 文件（带样式）
        html_content = html_path.read_text(encoding="utf-8")
        
        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>公众号文章预览</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .article-container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        h1, h2, h3 {{
            color: #333;
            margin-top: 1.5em;
            margin-bottom: 0.8em;
        }}
        p {{
            margin-bottom: 1em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="article-container">
        {html_content}
    </div>
</body>
</html>"""
        
        preview_path = self.output_dir / "preview.html"
        preview_path.write_text(full_html, encoding="utf-8")
        
        print(f"✅ 预览文件已生成: file://{preview_path.absolute()}")

    def _get_current_date(self) -> str:
        """获取当前日期"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    def run(
        self,
        url: str,
        style: str = "pm",
        theme: str = "科技蓝",
        skip_search: bool = False
    ):
        """执行完整流程"""

        print(f"\n🎯 开始处理抖音视频")
        print(f"📹 URL: {url}")
        print(f"✍️ 写作风格: {style}")
        print(f"🎨 配色主题: {theme}")

        try:
            # 步骤 1: 转写
            transcript_path = self.step1_transcribe(url)
            
            # 步骤 2: 搜索资料
            if skip_search:
                search_path = self.output_dir / "search_results.json"
                search_path.write_text("[]", encoding="utf-8")
            else:
                search_path = self.step2_search(transcript_path)
            
            # 步骤 3: 构思框架
            outline_path = self.step3_outline(transcript_path, search_path)
            
            # 步骤 4: 写作
            article_path = self.step4_write(transcript_path, outline_path, style)
            
            # 步骤 5: 格式化
            html_path = self.step5_format(article_path, theme)
            
            # 步骤 6: 预览
            self.step6_preview(html_path)
            
            # 输出总结
            print("\n" + "=" * 60)
            print("✅ 全部完成！")
            print("=" * 60)
            print(f"📄 转写文本: {self.output_dir / 'transcript.txt'}")
            print(f"🔍 搜索结果: {self.output_dir / 'search_results.json'}")
            print(f"💡 文章框架: {self.output_dir / 'outline.md'}")
            print(f"📝 Markdown: {self.output_dir / 'article.md'}")
            print(f"🎨 公众号HTML: {self.output_dir / 'article.html'}")
            print(f"👀 本地预览: file://{(self.output_dir / 'preview.html').absolute()}")
            print("\n💡 提示: 用浏览器打开 preview.html 即可预览效果")
            
            return True

        except Exception as e:
            print(f"\n❌ 处理失败: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    parser = argparse.ArgumentParser(description="抖音 → 公众号完整流程")
    parser.add_argument("url", help="抖音视频 URL")
    parser.add_argument("--style", "-s", default="pm", choices=["pm", "tech", "casual"],
                       help="写作风格 (pm=产品经理, tech=技术专家, casual=轻松口语)")
    parser.add_argument("--theme", default="科技蓝",
                       choices=["科技蓝", "活力橙", "高雅灰"],
                       help="配色主题")
    parser.add_argument("--output", "-o", default="output", help="输出目录")
    parser.add_argument("--skip-search", action="store_true", help="跳过搜索步骤")

    args = parser.parse_args()

    # 检查必需的环境变量
    required_vars = ["TIKHUB_API_KEY", "OPENAI_API_KEY"]
    missing = [v for v in required_vars if not os.getenv(v)]
    
    if missing:
        print(f"❌ 缺少环境变量: {', '.join(missing)}")
        print("请设置以下环境变量：")
        for var in missing:
            print(f"  export {var}='your-key-here'")
        sys.exit(1)

    # 执行流程
    pipeline = DouyinToWechatPipeline(Path(args.output))
    success = pipeline.run(
        url=args.url,
        style=args.style,
        theme=args.theme,
        skip_search=args.skip_search
    )

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
