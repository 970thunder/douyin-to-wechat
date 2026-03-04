#!/usr/bin/env python3
"""
公众号文章排版工具 - Markdown 转 HTML
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional
import re

class WechatFormatter:
    def __init__(self):
        self.themes = {
            "科技蓝": {
                "primary": "#1890FF",
                "secondary": "#69C0FF",
                "text": "#333333",
                "bg": "#F0F5FF"
            },
            "活力橙": {
                "primary": "#FF6B35",
                "secondary": "#FFA07A",
                "text": "#333333",
                "bg": "#FFF5F0"
            },
            "高雅灰": {
                "primary": "#333333",
                "secondary": "#666666",
                "text": "#333333",
                "bg": "#F5F5F5"
            },
            "清新绿": {
                "primary": "#52C41A",
                "secondary": "#95DE64",
                "text": "#333333",
                "bg": "#F6FFED"
            }
        }

    def parse_markdown(self, markdown_text: str) -> str:
        """解析 Markdown 为 HTML（简化版）"""

        lines = markdown_text.split('\n')
        html_lines = []

        in_code_block = False
        code_content = []
        code_lang = ""

        for line in lines:
            # 代码块
            if line.startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_lang = line[3:].strip()
                    code_content = []
                else:
                    in_code_block = False
                    html_lines.append(self._format_code_block(
                        '\n'.join(code_content),
                        code_lang
                    ))
                continue

            if in_code_block:
                code_content.append(line)
                continue

            # 标题
            if line.startswith('# '):
                html_lines.append(self._format_h1(line[2:]))
            elif line.startswith('## '):
                html_lines.append(self._format_h2(line[3:]))
            elif line.startswith('### '):
                html_lines.append(self._format_h3(line[4:]))

            # 引用
            elif line.startswith('> '):
                html_lines.append(self._format_quote(line[2:]))

            # 列表
            elif line.startswith('- '):
                html_lines.append(self._format_list_item(line[2:]))

            # 分隔线
            elif line.strip() == '---':
                html_lines.append('<hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">')

            # 普通段落
            elif line.strip():
                html_lines.append(self._format_paragraph(line))

        return '\n'.join(html_lines)

    def _format_h1(self, text: str) -> str:
        return f'''<h1 style="font-size: 24px; font-weight: bold; color: {{primary_color}}; margin: 20px 0 15px 0;">
{text}
</h1>'''

    def _format_h2(self, text: str) -> str:
        return f'''<h2 style="font-size: 20px; font-weight: bold; color: {{primary_color}}; margin: 18px 0 12px 0;">
{text}
</h2>'''

    def _format_h3(self, text: str) -> str:
        return f'''<h3 style="font-size: 18px; font-weight: bold; color: {{primary_color}}; margin: 15px 0 10px 0;">
{text}
</h3>'''

    def _format_paragraph(self, text: str) -> str:
        # 处理加粗
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # 处理斜体
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # 处理行内代码
        text = re.sub(r'`(.+?)`', r'<code style="background: #f5f5f5; padding: 2px 6px; border-radius: 3px;">\1</code>', text)

        return f'''<p style="font-size: 16px; line-height: 1.75; color: #333; margin: 10px 0; text-align: justify;">
{text}
</p>'''

    def _format_quote(self, text: str) -> str:
        return f'''<blockquote style="border-left: 4px solid {{primary_color}}; padding-left: 16px; margin: 15px 0; color: #666; font-style: italic;">
{text}
</blockquote>'''

    def _format_list_item(self, text: str) -> str:
        return f'''<li style="font-size: 16px; line-height: 1.75; color: #333; margin: 5px 0;">
{text}
</li>'''

    def _format_code_block(self, code: str, lang: str) -> str:
        return f'''<pre style="background: #282c34; color: #abb2bf; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 15px 0;">
<code style="font-family: 'Courier New', monospace; font-size: 14px;">
{self._escape_html(code)}
</code>
</pre>'''

    def _escape_html(self, text: str) -> str:
        """转义 HTML 特殊字符"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

    def apply_theme(self, html: str, theme_name: str) -> str:
        """应用主题样式"""
        theme = self.themes.get(theme_name, self.themes["科技蓝"])

        # 替换颜色占位符
        html = html.replace('{primary_color}', theme['primary'])
        html = html.replace('{secondary_color}', theme['secondary'])

        # 添加容器
        return f'''<section style="max-width: 677px; margin: 0 auto; padding: 20px; background: {theme['bg']};">
{html}
</section>'''

    def process(self, input_path: Path, theme: str = "科技蓝", output_path: Optional[Path] = None) -> str:
        """完整处理流程"""

        # 1. 读取 Markdown
        markdown_text = input_path.read_text(encoding="utf-8")

        # 2. 解析为 HTML
        html = self.parse_markdown(markdown_text)

        # 3. 应用主题
        html = self.apply_theme(html, theme)

        # 4. 保存
        if output_path:
            output_path.write_text(html, encoding="utf-8")
            print(f"✅ HTML 已保存: {output_path}")

        return html

def main():
    import argparse

    parser = argparse.ArgumentParser(description="公众号文章排版工具")
    parser.add_argument("--input", "-i", required=True, help="输入 Markdown 文件")
    parser.add_argument("--output", "-o", default="article.html", help="输出 HTML 文件")
    parser.add_argument("--theme", "-t", default="科技蓝",
                       choices=["科技蓝", "活力橙", "高雅灰", "清新绿"],
                       help="主题风格")
    parser.add_argument("--preview", "-p", action="store_true", help="预览（打开浏览器）")

    args = parser.parse_args()

    # 执行排版
    formatter = WechatFormatter()
    html = formatter.process(
        input_path=Path(args.input),
        theme=args.theme,
        output_path=Path(args.output)
    )

    print(f"\n✅ 排版完成！文件大小：{len(html)} 字节")

    # 预览
    if args.preview:
        import webbrowser
        webbrowser.open(f"file://{Path(args.output).absolute()}")
        print("🌐 已在浏览器中打开预览")

if __name__ == "__main__":
    main()
