#!/usr/bin/env python3
"""
产品经理视角的公众号文章写作
"""

import os
import sys
from pathlib import Path
from typing import Optional
import openai

class ProductManagerWriter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def read_input(self, input_path: Path) -> str:
        """读取输入文件"""
        return input_path.read_text(encoding="utf-8")

    def search_references(self, topic: str) -> str:
        """搜索相关资料（模拟）"""
        # 这里可以集成真实的搜索 API
        return f"相关资料：{topic}"

    def generate_article(
        self,
        content: str,
        style: str = "专业",
        topic: Optional[str] = None
    ) -> str:
        """生成公众号文章"""

        style_prompts = {
            "专业": "使用数据驱动、逻辑严密的写作风格，适合 B2B 和技术文章",
            "轻松": "使用故事化、口语化的写作风格，适合 B2C 和品牌传播",
            "干货": "使用实用技巧、可操作的写作风格，适合教程和指南"
        }

        prompt = f"""你是一位资深的产品经理，请基于以下内容撰写一篇公众号文章。

原始内容：
{content}

写作要求：
1. {style_prompts.get(style, style_prompts['专业'])}
2. 标题要吸引眼球
3. 使用清晰的结构和层次
4. 每个段落不要超过 200 字
5. 包含实际案例或数据支撑
6. 结尾给出明确的行动建议

文章结构：
# 标题

## 背景与痛点
[说明为什么这个问题重要，用户的痛点是什么]

## 解决方案
[核心思路和实现方法]

## 价值与收益
[用户和业务的价值]

## 行动建议
[下一步该做什么]

请输出完整的 Markdown 格式文章："""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一位经验丰富的产品经理和内容创作者"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=3000
        )

        article = response.choices[0].message.content

        # 添加元信息
        metadata = f"""---
title: 文章标题
author: 产品经理
date: {self._get_current_date()}
tags: [产品, 思考]
---

"""
        return metadata + article

    def _get_current_date(self) -> str:
        """获取当前日期"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    def add_cover_image(self, article: str, topic: str) -> str:
        """添加封面图（模拟）"""
        # 实际实现可以调用 Unsplash API
        cover_url = f"https://images.unsplash.com/photo-{hash(topic) % 1000000}"
        return article.replace("---\n", f"---\ncover: {cover_url}\n", 1)

    def process(
        self,
        input_path: Optional[Path] = None,
        topic: Optional[str] = None,
        style: str = "专业",
        output_path: Optional[Path] = None
    ) -> str:
        """完整处理流程"""

        # 1. 读取内容
        if input_path:
            content = self.read_input(input_path)
        elif topic:
            content = self.search_references(topic)
        else:
            raise ValueError("必须提供 input_path 或 topic")

        # 2. 生成文章
        article = self.generate_article(content, style, topic)

        # 3. 添加封面图
        article = self.add_cover_image(article, topic or input_path.stem)

        # 4. 保存文章
        if output_path:
            output_path.write_text(article, encoding="utf-8")
            print(f"✅ 文章已保存: {output_path}")

        return article

def main():
    import argparse

    parser = argparse.ArgumentParser(description="产品经理视角文章写作")
    parser.add_argument("--input", "-i", help="输入文件路径")
    parser.add_argument("--topic", "-t", help="文章主题")
    parser.add_argument("--output", "-o", default="article.md", help="输出文件路径")
    parser.add_argument("--style", "-s", default="专业", choices=["专业", "轻松", "干货"],
                       help="写作风格")

    args = parser.parse_args()

    # 获取 API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 错误：请设置 OPENAI_API_KEY 环境变量")
        sys.exit(1)

    # 执行写作
    writer = ProductManagerWriter(api_key)
    article = writer.process(
        input_path=Path(args.input) if args.input else None,
        topic=args.topic,
        style=args.style,
        output_path=Path(args.output)
    )

    print(f"\n✅ 文章生成完成！字数：{len(article)}")

if __name__ == "__main__":
    main()
