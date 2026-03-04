#!/usr/bin/env python3
"""
抖音视频转写脚本
功能：下载视频 → 提取音频 → Whisper 转写 → 生成总结
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from typing import Optional
import openai

class DouyinTranscriber:
    def __init__(self, tikhub_api_key: str, openai_api_key: str):
        self.tikhub_api_key = tikhub_api_key
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key

    def download_video(self, url: str, output_dir: Path) -> Path:
        """使用 Tikhub API 下载抖音视频"""
        print(f"📥 正在下载视频: {url}")

        # Tikhub API 调用
        api_url = "https://api.tikhub.io/v1/douyin/video/download"
        headers = {
            "Authorization": f"Bearer {self.tikhub_api_key}",
            "Content-Type": "application/json"
        }
        data = {"url": url}

        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()

        # 下载视频文件
        video_url = response.json()["data"]["video_url"]
        video_path = output_dir / "video.mp4"

        video_response = requests.get(video_url)
        video_path.write_bytes(video_response.content)

        print(f"✅ 视频已下载: {video_path}")
        return video_path

    def extract_audio(self, video_path: Path, output_dir: Path) -> Path:
        """使用 ffmpeg 提取音频"""
        print(f"🎵 正在提取音频...")

        audio_path = output_dir / "audio.mp3"

        cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-vn",
            "-acodec", "mp3",
            "-ab", "192k",
            "-y",
            str(audio_path)
        ]

        subprocess.run(cmd, check=True, capture_output=True)

        print(f"✅ 音频已提取: {audio_path}")
        return audio_path

    def transcribe_audio(self, audio_path: Path) -> str:
        """使用 OpenAI Whisper API 转写音频"""
        print(f"📝 正在转写音频...")

        with open(audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language="zh"
            )

        print(f"✅ 转写完成")
        return transcript.text

    def generate_summary(self, transcript: str) -> str:
        """使用 GPT-4 生成总结"""
        print(f"🤖 正在生成总结...")

        prompt = f"""请分析以下抖音视频的转写内容，生成一份结构化的总结文档：

转写内容：
{transcript}

请按以下格式输出：

# 视频总结

## 核心观点
1. [观点1]
2. [观点2]
3. [观点3]

## 关键内容

### 第一部分
[内容摘要]

### 第二部分
[内容摘要]

## 金句摘录
- "[金句1]"
- "[金句2]"

## 行动建议
- [建议1]
- [建议2]
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一位专业的内容分析师"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        summary = response.choices[0].message.content
        print(f"✅ 总结已生成")
        return summary

    def process(self, url: str, output_dir: Optional[Path] = None) -> dict:
        """完整处理流程"""
        if output_dir is None:
            output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. 下载视频
        video_path = self.download_video(url, output_dir)

        # 2. 提取音频
        audio_path = self.extract_audio(video_path, output_dir)

        # 3. 转写音频
        transcript = self.transcribe_audio(audio_path)

        # 保存转写文本
        transcript_path = output_dir / "transcript.txt"
        transcript_path.write_text(transcript, encoding="utf-8")

        # 4. 生成总结
        summary = self.generate_summary(transcript)

        # 保存总结
        summary_path = output_dir / "summary.md"
        summary_path.write_text(summary, encoding="utf-8")

        return {
            "video": str(video_path),
            "audio": str(audio_path),
            "transcript": str(transcript_path),
            "summary": str(summary_path)
        }

def main():
    import argparse

    parser = argparse.ArgumentParser(description="抖音视频转写工具")
    parser.add_argument("url", help="抖音视频 URL")
    parser.add_argument("--output", "-o", default="output", help="输出目录")
    parser.add_argument("--no-summary", action="store_true", help="不生成总结")

    args = parser.parse_args()

    # 获取 API keys
    tikhub_api_key = os.getenv("TIKHUB_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not tikhub_api_key or not openai_api_key:
        print("❌ 错误：请设置 TIKHUB_API_KEY 和 OPENAI_API_KEY 环境变量")
        sys.exit(1)

    # 执行转写
    transcriber = DouyinTranscriber(tikhub_api_key, openai_api_key)
    result = transcriber.process(args.url, Path(args.output))

    print("\n✅ 处理完成！")
    print(f"📄 转写文本: {result['transcript']}")
    print(f"📊 核心总结: {result['summary']}")

if __name__ == "__main__":
    main()
