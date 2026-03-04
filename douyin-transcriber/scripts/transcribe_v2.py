#!/usr/bin/env python3
"""
抖音视频转写脚本 - 支持多种转写引擎
免费方案：Whisper.cpp / FunASR / PaddleSpeech
付费方案：OpenAI Whisper API
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional
import requests

class DouyinTranscriber:
    def __init__(
        self,
        tikhub_api_key: str,
        whisper_engine: str = "whisper.cpp",
        openai_api_key: Optional[str] = None
    ):
        self.tikhub_api_key = tikhub_api_key
        self.whisper_engine = whisper_engine
        self.openai_api_key = openai_api_key

    def download_video(self, url: str, output_dir: Path) -> Path:
        """使用 Tikhub API 下载抖音视频"""
        print(f"📥 正在下载视频: {url}")

        # 使用正确的 Tikhub API 端点（GET 方法）
        api_url = "https://api.tikhub.io/api/v1/douyin/web/fetch_one_video_by_share_url"
        headers = {
            "Authorization": f"Bearer {self.tikhub_api_key}"
        }
        params = {"share_url": url}

        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()

        result = response.json()
        if "data" not in result or "aweme_detail" not in result["data"]:
            raise Exception(f"API 返回数据格式错误: {result}")

        video_url = result["data"]["aweme_detail"]["video"]["play_addr"]["url_list"][0]
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
        """转写音频 - 支持多种引擎"""

        if self.whisper_engine == "whisper.cpp":
            return self._transcribe_whisper_cpp(audio_path)
        elif self.whisper_engine == "funasr":
            return self._transcribe_funasr(audio_path)
        elif self.whisper_engine == "paddlespeech":
            return self._transcribe_paddlespeech(audio_path)
        elif self.whisper_engine == "openai":
            return self._transcribe_openai(audio_path)
        else:
            raise ValueError(f"不支持的引擎: {self.whisper_engine}")

    def _transcribe_whisper_cpp(self, audio_path: Path) -> str:
        """使用 Whisper.cpp 转写（免费）"""
        print(f"📝 正在使用 Whisper.cpp 转写...")

        output_txt = audio_path.parent / "transcript_raw.txt"
        
        # 使用下载的模型文件路径
        model_path = Path.home() / ".cache" / "whisper" / "ggml-base.bin"
        
        if not model_path.exists():
            raise Exception(f"Whisper 模型文件不存在: {model_path}\n请先下载模型")

        # Homebrew 安装的命令是 whisper-cli
        cmd = [
            "whisper-cli",
            "-f", str(audio_path),
            "-l", "zh",
            "-m", str(model_path),
            "-otxt",
            "-of", str(output_txt.with_suffix(''))
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            transcript = output_txt.read_text(encoding="utf-8")
            print(f"✅ Whisper.cpp 转写完成")
            return transcript
        except FileNotFoundError:
            raise Exception("Whisper.cpp 未安装，请运行: brew install whisper-cpp")

    def _transcribe_funasr(self, audio_path: Path) -> str:
        """使用 FunASR 转写（免费）"""
        print(f"📝 正在使用 FunASR 转写...")

        try:
            from funasr import AutoModel

            model = AutoModel(model="paraformer-zh")
            result = model.generate(input=str(audio_path))

            transcript = result[0]["text"]
            print(f"✅ FunASR 转写完成")
            return transcript
        except ImportError:
            raise Exception("FunASR 未安装，请运行: pip install funasr")

    def _transcribe_paddlespeech(self, audio_path: Path) -> str:
        """使用 PaddleSpeech 转写（免费）"""
        print(f"📝 正在使用 PaddleSpeech 转写...")

        try:
            from paddlespeech.cli import ASRExecutor

            asr = ASRExecutor()
            result = asr(audio_file=str(audio_path))

            print(f"✅ PaddleSpeech 转写完成")
            return result
        except ImportError:
            raise Exception("PaddleSpeech 未安装，请运行: pip install paddlespeech")

    def _transcribe_openai(self, audio_path: Path) -> str:
        """使用 OpenAI Whisper API 转写（付费）"""
        print(f"📝 正在使用 OpenAI Whisper 转写...")

        if not self.openai_api_key:
            raise ValueError("OpenAI API Key 未配置")

        import openai
        openai.api_key = self.openai_api_key

        with open(audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language="zh"
            )

        print(f"✅ OpenAI Whisper 转写完成")
        return transcript.text

    def generate_summary(self, transcript: str, api_key: str) -> str:
        """生成总结（使用 DeepSeek/OpenAI）"""
        print(f"🤖 正在生成总结...")

        from openai import OpenAI
        
        # 支持 DeepSeek API
        base_url = os.getenv("OPENAI_BASE_URL")
        client = OpenAI(api_key=api_key, base_url=base_url)

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

        response = client.chat.completions.create(
            model="deepseek-chat",
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

    def process(
        self,
        url: str,
        output_dir: Optional[Path] = None,
        openai_api_key: Optional[str] = None
    ) -> dict:
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

        # 4. 生成总结（如果提供了 OpenAI API Key）
        if openai_api_key:
            summary = self.generate_summary(transcript, openai_api_key)
            summary_path = output_dir / "summary.md"
            summary_path.write_text(summary, encoding="utf-8")
        else:
            print("⚠️ 未提供 OpenAI API Key，跳过总结生成")
            summary_path = None

        return {
            "video": str(video_path),
            "audio": str(audio_path),
            "transcript": str(transcript_path),
            "summary": str(summary_path) if summary_path else None
        }

def main():
    import argparse

    parser = argparse.ArgumentParser(description="抖音视频转写工具")
    parser.add_argument("url", help="抖音视频 URL")
    parser.add_argument("--output", "-o", default="output", help="输出目录")
    parser.add_argument("--engine", "-e", default="whisper.cpp",
                       choices=["whisper.cpp", "funasr", "paddlespeech", "openai"],
                       help="转写引擎")
    parser.add_argument("--no-summary", action="store_true", help="不生成总结")

    args = parser.parse_args()

    # 获取 API keys
    tikhub_api_key = os.getenv("TIKHUB_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not tikhub_api_key:
        print("❌ 错误：请设置 TIKHUB_API_KEY 环境变量")
        sys.exit(1)

    if args.engine == "openai" and not openai_api_key:
        print("❌ 错误：使用 OpenAI 引擎需要设置 OPENAI_API_KEY")
        sys.exit(1)

    # 执行转写
    transcriber = DouyinTranscriber(
        tikhub_api_key=tikhub_api_key,
        whisper_engine=args.engine,
        openai_api_key=openai_api_key
    )

    result = transcriber.process(
        url=args.url,
        output_dir=Path(args.output),
        openai_api_key=openai_api_key if not args.no_summary else None
    )

    print("\n✅ 处理完成！")
    print(f"📄 转写文本: {result['transcript']}")
    if result['summary']:
        print(f"📊 核心总结: {result['summary']}")

if __name__ == "__main__":
    main()
