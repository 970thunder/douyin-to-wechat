#!/usr/bin/env python3
"""
快速配置脚本 - 一键设置抖音转写系统
"""

import os
import sys
from pathlib import Path

def check_command(cmd: str) -> bool:
    """检查命令是否存在"""
    import shutil
    return shutil.which(cmd) is not None

def install_whisper_cpp():
    """安装 Whisper.cpp"""
    print("\n📦 正在安装 Whisper.cpp...")

    if check_command("brew"):
        os.system("brew install whisper-cpp")
        print("✅ Whisper.cpp 已安装")
        return True
    else:
        print("❌ 未找到 Homebrew，请手动安装")
        print("   安装命令: brew install whisper-cpp")
        return False

def install_funasr():
    """安装 FunASR"""
    print("\n📦 正在安装 FunASR...")

    result = os.system("pip install funasr modelscope")
    if result == 0:
        print("✅ FunASR 已安装")
        return True
    else:
        print("❌ FunASR 安装失败")
        return False

def create_env_file(tikhub_key: str):
    """创建 .env 配置文件"""
    print("\n📝 正在创建配置文件...")

    env_content = f"""# ========== 必需配置 ==========

# Tikhub API Key（抖音视频下载）
TIKHUB_API_KEY={tikhub_key}

# ========== 转写引擎配置 ==========

# 转写引擎 (whisper.cpp / funasr / paddlespeech / openai)
WHISPER_ENGINE=whisper.cpp

# Whisper.cpp 模型 (tiny / base / small / medium / large)
WHISPER_MODEL=base

# ========== 可选配置 ==========

# OpenAI API Key（用于生成总结）
OPENAI_API_KEY=

# 微信公众号 AppID（用于发布）
WECHAT_APPID=

# 微信公众号 AppSecret（用于发布）
WECHAT_APPSECRET=
"""

    env_path = Path(".env")
    env_path.write_text(env_content, encoding="utf-8")

    print(f"✅ 配置文件已创建: {env_path.absolute()}")
    print("\n💡 提示: 如需生成总结，请编辑 .env 文件添加 OPENAI_API_KEY")

def test_installation():
    """测试安装是否成功"""
    print("\n🧪 正在测试安装...")

    # 检查 Whisper.cpp
    if check_command("whisper-cpp"):
        print("  ✅ Whisper.cpp 已安装")
    else:
        print("  ❌ Whisper.cpp 未安装")

    # 检查 Python 依赖
    try:
        import requests
        print("  ✅ requests 已安装")
    except ImportError:
        print("  ❌ requests 未安装")

    print("\n💡 如有缺失，请运行: pip install -r requirements.txt")

def main():
    print("="*60)
    print("🚀 抖音转写系统 - 快速配置")
    print("="*60)

    # 1. 检查系统依赖
    print("\n🔍 检查系统依赖...")

    if not check_command("ffmpeg"):
        print("❌ ffmpeg 未安装")
        print("   安装命令: brew install ffmpeg")
        return

    if not check_command("python3"):
        print("❌ Python3 未安装")
        return

    print("✅ 系统依赖已满足")

    # 2. 选择转写引擎
    print("\n🎯 选择转写引擎:")
    print("1. Whisper.cpp（推荐 - 完全免费，质量高）")
    print("2. FunASR（免费，中文优化）")
    print("3. 跳过（稍后手动安装）")

    choice = input("\n请选择 [1/2/3]: ").strip()

    if choice == "1":
        install_whisper_cpp()
    elif choice == "2":
        install_funasr()
    else:
        print("⏭️  跳过安装")

    # 3. 配置 Tikhub API Key
    print("\n🔑 配置 Tikhub API Key")
    tikhub_key = input("请输入 Tikhub API Key: ").strip()

    if not tikhub_key:
        print("❌ Tikhub API Key 不能为空")
        return

    # 4. 创建配置文件
    create_env_file(tikhub_key)

    # 5. 测试安装
    test_installation()

    # 6. 完成
    print("\n" + "="*60)
    print("✅ 配置完成！")
    print("="*60)
    print("\n📖 快速开始:")
    print("1. 测试系统: python scripts/test_workflow.py")
    print("2. 转写视频: python scripts/transcribe_v2.py '抖音URL'")
    print("3. 查看文档: cat FREE_TRANSCRIPTION.md")

if __name__ == "__main__":
    main()
