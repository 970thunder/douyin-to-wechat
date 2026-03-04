#!/usr/bin/env python3
"""
测试脚本 - 验证所有组件是否正常工作
"""

import os
import sys
from pathlib import Path

def test_dependencies():
    """测试依赖是否安装"""
    print("🔍 检查依赖...")

    dependencies = {
        "openai": "OpenAI Python SDK",
        "requests": "HTTP 请求库"
    }

    missing = []
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name}")
            missing.append(module)

    if missing:
        print(f"\n请安装缺失的依赖: pip install {' '.join(missing)}")
        return False

    return True

def test_api_keys():
    """测试 API Keys 是否配置"""
    print("\n🔑 检查 API Keys...")

    keys = {
        "TIKHUB_API_KEY": "Tikhub API",
        "OPENAI_API_KEY": "OpenAI API",
        "WECHAT_APPID": "微信 AppID",
        "WECHAT_APPSECRET": "微信 AppSecret"
    }

    missing = []
    for key, name in keys.items():
        if os.getenv(key):
            print(f"  ✅ {name}: {os.getenv(key)[:10]}...")
        else:
            print(f"  ❌ {name}: 未配置")
            missing.append(key)

    if missing:
        print(f"\n请配置环境变量:")
        for key in missing:
            print(f"  export {key}='your_key'")

    return len(missing) == 0

def test_ffmpeg():
    """测试 ffmpeg 是否安装"""
    print("\n🎬 检查 ffmpeg...")

    import subprocess
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True
        )
        version = result.stdout.split('\n')[0]
        print(f"  ✅ {version}")
        return True
    except FileNotFoundError:
        print("  ❌ ffmpeg 未安装")
        print("  安装: brew install ffmpeg")
        return False

def test_scripts():
    """测试脚本是否存在"""
    print("\n📜 检查脚本...")

    scripts = [
        "douyin-transcriber/scripts/transcribe.py",
        "wechat-product-manager-writer/scripts/writer.py",
        "wechat-tech-writer/scripts/tech_writer.py",
        "wechat-article-formatter/scripts/formatter.py",
        "wechat-draft-publisher/scripts/publisher.py"
    ]

    all_exist = True
    for script in scripts:
        path = Path(__file__).parent.parent / script
        if path.exists():
            print(f"  ✅ {script}")
        else:
            print(f"  ❌ {script}")
            all_exist = False

    return all_exist

def test_api_connections():
    """测试 API 连接"""
    print("\n🌐 测试 API 连接...")

    # 测试 OpenAI
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.Model.list()
        print("  ✅ OpenAI API 连接正常")
    except Exception as e:
        print(f"  ❌ OpenAI API 连接失败: {e}")
        return False

    # 测试微信 API
    try:
        import requests
        appid = os.getenv("WECHAT_APPID")
        appsecret = os.getenv("WECHAT_APPSECRET")

        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
        response = requests.get(url)
        data = response.json()

        if "access_token" in data:
            print("  ✅ 微信 API 连接正常")
        else:
            print(f"  ❌ 微信 API 连接失败: {data.get('errmsg', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"  ❌ 微信 API 连接失败: {e}")
        return False

    return True

def main():
    print("="*60)
    print("🧪 抖音 → 公众号系统测试")
    print("="*60)

    tests = [
        ("依赖", test_dependencies),
        ("API Keys", test_api_keys),
        ("ffmpeg", test_ffmpeg),
        ("脚本文件", test_scripts),
    ]

    # 只在 API Keys 配置后才测试连接
    if os.getenv("OPENAI_API_KEY") and os.getenv("WECHAT_APPID"):
        tests.append(("API 连接", test_api_connections))

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
        print("\n🎉 所有测试通过！系统已就绪。")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查配置。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
