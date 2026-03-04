#!/usr/bin/env python3
"""
技术专家视角的公众号文章写作
"""

import os
import sys
from pathlib import Path
from typing import Optional
import openai

class TechWriter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def read_input(self, input_path: Path) -> str:
        """读取输入文件"""
        return input_path.read_text(encoding="utf-8")

    def analyze_code(self, code: str) -> str:
        """分析代码（如果输入是代码）"""
        return f"代码分析：{len(code)} 行"

    def generate_article(
        self,
        content: str,
        level: str = "进阶",
        stack: Optional[str] = None
    ) -> str:
        """生成技术文章"""

        level_prompts = {
            "入门": "面向初学者，概念为主，少量代码，详细解释",
            "进阶": "面向工程师，原理+实践，包含完整代码示例",
            "高级": "面向架构师，源码分析+性能优化+最佳实践"
        }

        prompt = f"""你是一位技术专家，请基于以下内容撰写一篇深度技术文章。

原始内容：
{content}

技术栈：{stack or "通用"}

写作要求：
1. {level_prompts.get(level, level_prompts['进阶'])}
2. 代码必须有完整注释
3. 包含架构图或流程图（使用 Mermaid 语法）
4. 提供性能对比数据
5. 给出最佳实践建议
6. 避免废话，直奔主题

文章结构：
# 技术标题

## 背景与问题
[技术背景和遇到的问题]

## 技术方案
### 架构设计
[整体架构]
### 核心原理
[技术原理]
### 实现细节
[代码示例]

## 性能优化
[优化方案和对比数据]

## 最佳实践
[踩坑经验]

## 总结
[关键收获]

请输出完整的 Markdown 格式文章，包含代码块和 Mermaid 图表："""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一位资深的技术专家和架构师"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )

        article = response.choices[0].message.content

        # 添加元信息
        metadata = f"""---
title: 技术文章标题
author: 技术专家
date: {self._get_current_date()}
tags: [技术, {stack or '通用'}]
---

"""
        return metadata + article

    def _get_current_date(self) -> str:
        """获取当前日期"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    def add_code_examples(self, article: str, stack: str) -> str:
        """补充代码示例（如果需要）"""
        # 实际实现可以生成更完整的代码示例
        return article

    def process(
        self,
        input_path: Optional[Path] = None,
        repo: Optional[str] = None,
        level: str = "进阶",
        stack: Optional[str] = None,
        output_path: Optional[Path] = None
    ) -> str:
        """完整处理流程"""

        # 1. 读取内容
        if input_path:
            content = self.read_input(input_path)
        elif repo:
            content = f"代码仓库：{repo}"
        else:
            raise ValueError("必须提供 input_path 或 repo")

        # 2. 生成文章
        article = self.generate_article(content, level, stack)

        # 3. 补充代码示例
        article = self.add_code_examples(article, stack or "Python")

        # 4. 保存文章
        if output_path:
            output_path.write_text(article, encoding="utf-8")
            print(f"✅ 文章已保存: {output_path}")

        return article

def main():
    import argparse

    parser = argparse.ArgumentParser(description="技术专家视角文章写作")
    parser.add_argument("--input", "-i", help="输入文件路径")
    parser.add_argument("--repo", "-r", help="代码仓库 URL")
    parser.add_argument("--output", "-o", default="article.md", help="输出文件路径")
    parser.add_argument("--level", "-l", default="进阶",
                       choices=["入门", "进阶", "高级"],
                       help="技术深度")
    parser.add_argument("--stack", "-s", help="技术栈（如：Python, FastAPI）")

    args = parser.parse_args()

    # 获取 API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 错误：请设置 OPENAI_API_KEY 环境变量")
        sys.exit(1)

    # 执行写作
    writer = TechWriter(api_key)
    article = writer.process(
        input_path=Path(args.input) if args.input else None,
        repo=args.repo,
        level=args.level,
        stack=args.stack,
        output_path=Path(args.output)
    )

    print(f"\n✅ 技术文章生成完成！字数：{len(article)}")

if __name__ == "__main__":
    main()
