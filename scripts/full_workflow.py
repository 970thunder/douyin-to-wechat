#!/usr/bin/env python3
"""
抖音 → 公众号完整流程脚本
一键执行：转写 → 写作 → 排版 → 发布
"""

import os
import sys
from pathlib import Path
import argparse
import subprocess

class DouyinToWechatPipeline:
    def __init__(self, output_dir: Path = Path("output")):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def check_dependencies(self) -> bool:
        """检查依赖是否安装"""
        dependencies = ["ffmpeg", "python3"]

        for dep in dependencies:
            try:
                subprocess.run([dep, "--version"], capture_output=True, check=True)
            except:
                print(f"❌ 缺少依赖: {dep}")
                return False

        return True

    def check_api_keys(self) -> bool:
        """检查 API Keys"""
        required_keys = [
            "TIKHUB_API_KEY",
            "OPENAI_API_KEY",
            "WECHAT_APPID",
            "WECHAT_APPSECRET"
        ]

        missing = []
        for key in required_keys:
            if not os.getenv(key):
                missing.append(key)

        if missing:
            print(f"❌ 缺少环境变量: {', '.join(missing)}")
            return False

        return True

    def step1_transcribe(self, url: str) -> Path:
        """步骤 1: 视频转写"""
        print("\n" + "="*60)
        print("📹 步骤 1: 视频转写")
        print("="*60)

        from douyin_transcriber import DouyinTranscriber

        transcriber = DouyinTranscriber(
            tikhub_api_key=os.getenv("TIKHUB_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        result = transcriber.process(url, self.output_dir)
        return Path(result["summary"])

    def step2_write(self, summary_path: Path, style: str = "pm") -> Path:
        """步骤 2: 文章写作"""
        print("\n" + "="*60)
        print("✍️ 步骤 2: 文章写作")
        print("="*60)

        if style == "pm":
            from wechat_pm_writer import ProductManagerWriter
            writer = ProductManagerWriter(os.getenv("OPENAI_API_KEY"))
        else:
            from wechat_tech_writer import TechWriter
            writer = TechWriter(os.getenv("OPENAI_API_KEY"))

        article_path = self.output_dir / "article.md"
        writer.process(
            input_path=summary_path,
            style="专业" if style == "pm" else "进阶",
            output_path=article_path
        )

        return article_path

    def step3_format(self, article_path: Path, theme: str = "科技蓝") -> Path:
        """步骤 3: 排版美化"""
        print("\n" + "="*60)
        print("🎨 步骤 3: 排版美化")
        print("="*60)

        from wechat_formatter import WechatFormatter

        formatter = WechatFormatter()
        html_path = self.output_dir / "article.html"

        formatter.process(
            input_path=article_path,
            theme=theme,
            output_path=html_path
        )

        return html_path

    def step4_publish(self, html_path: Path, title: str, dry_run: bool = False) -> dict:
        """步骤 4: 发布草稿"""
        print("\n" + "="*60)
        print("🚀 步骤 4: 发布草稿")
        print("="*60)

        if dry_run:
            print("⚠️ Dry run 模式，跳过发布")
            return {"status": "dry_run"}

        from wechat_publisher import WechatPublisher, load_config

        config = load_config("main")
        publisher = WechatPublisher(config)

        result = publisher.publish(
            input_path=html_path,
            title=title
        )

        return result

    def run(
        self,
        url: str,
        title: str,
        style: str = "pm",
        theme: str = "科技蓝",
        dry_run: bool = False
    ):
        """执行完整流程"""

        print(f"\n🎯 开始处理: {url}")
        print(f"📝 文章标题: {title}")
        print(f"✍️ 写作风格: {style}")
        print(f"🎨 排版主题: {theme}")

        # 检查依赖
        if not self.check_dependencies():
            return False

        # 检查 API Keys
        if not dry_run and not self.check_api_keys():
            return False

        try:
            # 步骤 1: 转写
            summary_path = self.step1_transcribe(url)

            # 步骤 2: 写作
            article_path = self.step2_write(summary_path, style)

            # 步骤 3: 排版
            html_path = self.step3_format(article_path, theme)

            # 步骤 4: 发布
            result = self.step4_publish(html_path, title, dry_run)

            # 输出结果
            print("\n" + "="*60)
            print("✅ 处理完成！")
            print("="*60)
            print(f"📄 转写文本: {self.output_dir / 'transcript.txt'}")
            print(f"📊 核心总结: {summary_path}")
            print(f"📝 Markdown: {article_path}")
            print(f"🎨 HTML: {html_path}")

            if not dry_run:
                print(f"🔗 草稿链接: {result.get('url', 'N/A')}")

            return True

        except Exception as e:
            print(f"\n❌ 处理失败: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    parser = argparse.ArgumentParser(description="抖音 → 公众号完整流程")
    parser.add_argument("url", help="抖音视频 URL")
    parser.add_argument("--title", "-t", required=True, help="文章标题")
    parser.add_argument("--style", "-s", default="pm", choices=["pm", "tech"],
                       help="写作风格 (pm=产品经理, tech=技术专家)")
    parser.add_argument("--theme", default="科技蓝",
                       choices=["科技蓝", "活力橙", "高雅灰", "清新绿"],
                       help="排版主题")
    parser.add_argument("--output", "-o", default="output", help="输出目录")
    parser.add_argument("--dry-run", action="store_true", help="只生成，不发布")

    args = parser.parse_args()

    # 执行流程
    pipeline = DouyinToWechatPipeline(Path(args.output))
    success = pipeline.run(
        url=args.url,
        title=args.title,
        style=args.style,
        theme=args.theme,
        dry_run=args.dry_run
    )

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
