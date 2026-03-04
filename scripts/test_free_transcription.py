#!/usr/bin/env python3
"""
测试免费转写方案
"""

import os
import sys
from pathlib import Path

def test_whisper_cpp():
    """测试 Whisper.cpp"""
    print("\n🧪 测试 Whisper.cpp...")

    import subprocess
    try:
        # Homebrew 安装的命令是 whisper-cli
        result = subprocess.run(
            ["whisper-cli", "--help"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("  ✅ Whisper.cpp 已安装")
            return True
        else:
            print("  ❌ Whisper.cpp 安装异常")
            return False
    except FileNotFoundError:
        print("  ❌ Whisper.cpp 未安装")
        print("  💡 安装: brew install whisper-cpp")
        return False

def test_funasr():
    """测试 FunASR"""
    print("\n🧪 测试 FunASR...")

    try:
        import funasr
        print("  ✅ FunASR 已安装")

        # 测试加载模型
        print("  🔄 测试加载模型（首次需要下载，请耐心等待）...")
        from funasr import AutoModel
        model = AutoModel(model="paraformer-zh")
        print("  ✅ 模型加载成功")
        return True

    except ImportError:
        print("  ❌ FunASR 未安装")
        print("  💡 安装: pip install funasr modelscope")
        return False
    except Exception as e:
        print(f"  ❌ FunASR 测试失败: {e}")
        return False

def test_tikhub():
    """测试 Tikhub API"""
    print("\n🧪 测试 Tikhub API...")

    # 加载 .env 文件
    from pathlib import Path
    import os
    
    env_file = Path(".env")
    if env_file.exists():
        for line in env_file.read_text().split('\n'):
            if line.startswith('TIKHUB_API_KEY='):
                os.environ['TIKHUB_API_KEY'] = line.split('=', 1)[1]
                break
    
    tikhub_key = os.getenv("TIKHUB_API_KEY")

    if not tikhub_key:
        print("  ❌ TIKHUB_API_KEY 未配置")
        print("  💡 配置: export TIKHUB_API_KEY='your_key'")
        return False

    print(f"  ✅ TIKHUB_API_KEY 已配置: {tikhub_key[:10]}...")
    return True

def test_transcribe():
    """测试转写功能（使用测试音频）"""
    print("\n🧪 测试转写功能...")

    # 创建测试音频（1秒静音）
    import subprocess

    test_audio = Path("test_audio.mp3")

    if not test_audio.exists():
        print("  🔄 创建测试音频...")
        subprocess.run([
            "ffmpeg",
            "-f", "lavfi",
            "-i", "anullsrc=r=16000:cl=mono",
            "-t", "1",
            "-y",
            str(test_audio)
        ], capture_output=True)

    # 测试 Whisper.cpp 转写（使用 whisper-cli 命令）
    print("  🔄 测试 Whisper.cpp 转写...")
    result = subprocess.run([
        "whisper-cli",
        "-f", str(test_audio),
        "-l", "zh",
        "-m", str(Path.home() / ".cache/whisper/ggml-base.bin"),
        "-otxt",
        "-of", "test_transcript"
    ], capture_output=True)

    if result.returncode == 0:
        print("  ✅ Whisper.cpp 转写成功")

        # 清理测试文件
        test_audio.unlink(missing_ok=True)
        Path("test_transcript.txt").unlink(missing_ok=True)

        return True
    else:
        print(f"  ❌ Whisper.cpp 转写失败: {result.stderr.decode()}")
        return False

def main():
    print("="*60)
    print("🧪 免费转写方案测试")
    print("="*60)

    tests = [
        ("Tikhub API", test_tikhub),
        ("Whisper.cpp", test_whisper_cpp),
        ("FunASR", test_funasr),
        ("转写功能", test_transcribe)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} 测试出错: {e}")
            results.append((name, False))

    # 总结
    print("\n" + "="*60)
    print("📊 测试结果")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:20} {status}")

    print(f"\n通过率: {passed}/{total} ({passed/total*100:.0f}%)")

    if passed == total:
        print("\n🎉 所有测试通过！免费转写方案已就绪。")
        print("\n📖 使用方法:")
        print("  python scripts/transcribe_v2.py '抖音URL' --engine whisper.cpp")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请参考以下指南:")
        print("  📖 免费方案安装: cat FREE_TRANSCRIPTION.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
