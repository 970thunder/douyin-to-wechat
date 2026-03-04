#!/usr/bin/env python3
"""
公众号草稿发布工具 - 调用微信 API
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class WechatConfig:
    appid: str
    appsecret: str
    access_token: Optional[str] = None
    token_expires: int = 0

class WechatPublisher:
    def __init__(self, config: WechatConfig):
        self.config = config
        self.base_url = "https://api.weixin.qq.com/cgi-bin"

    def get_access_token(self) -> str:
        """获取 Access Token"""

        # 检查是否过期
        if self.config.access_token and time.time() < self.config.token_expires:
            return self.config.access_token

        print("🔑 正在获取 Access Token...")

        url = f"{self.base_url}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.config.appid,
            "secret": self.config.appsecret
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "errcode" in data:
            raise Exception(f"获取 Access Token 失败: {data['errmsg']}")

        self.config.access_token = data["access_token"]
        self.config.token_expires = int(time.time()) + data["expires_in"] - 300  # 提前 5 分钟过期

        print(f"✅ Access Token 已获取，有效期：{data['expires_in']} 秒")
        return self.config.access_token

    def upload_image(self, image_path: Path) -> str:
        """上传图片素材"""

        print(f"📸 正在上传图片: {image_path}")

        access_token = self.get_access_token()
        url = f"{self.base_url}/material/add_material"

        with open(image_path, "rb") as f:
            files = {"media": f}
            params = {
                "access_token": access_token,
                "type": "image"
            }
            response = requests.post(url, params=params, files=files)

        data = response.json()

        if "errcode" in data:
            raise Exception(f"上传图片失败: {data['errmsg']}")

        print(f"✅ 图片已上传，media_id: {data['media_id']}")
        return data["media_id"]

    def create_draft(
        self,
        title: str,
        content: str,
        thumb_media_id: Optional[str] = None,
        author: str = "作者",
        digest: str = "",
        content_source_url: str = ""
    ) -> str:
        """创建草稿"""

        print(f"📝 正在创建草稿: {title}")

        access_token = self.get_access_token()
        url = f"{self.base_url}/draft/add"

        # 构建文章数据
        article = {
            "title": title,
            "author": author,
            "content": content,
            "digest": digest or content[:120],  # 默认取前 120 字
            "content_source_url": content_source_url,
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }

        # 添加封面图
        if thumb_media_id:
            article["thumb_media_id"] = thumb_media_id

        data = {
            "articles": [article]
        }

        response = requests.post(
            f"{url}?access_token={access_token}",
            json=data
        )

        result = response.json()

        if "errcode" in result:
            raise Exception(f"创建草稿失败: {result['errmsg']}")

        print(f"✅ 草稿已创建，media_id: {result['media_id']}")
        return result["media_id"]

    def get_draft(self, media_id: str) -> Dict:
        """获取草稿详情"""

        access_token = self.get_access_token()
        url = f"{self.base_url}/draft/get"

        response = requests.post(
            f"{url}?access_token={access_token}",
            json={"media_id": media_id}
        )

        return response.json()

    def publish(self, input_path: Path, title: Optional[str] = None, cover_image: Optional[Path] = None) -> Dict:
        """完整发布流程"""

        # 1. 读取 HTML 内容
        content = input_path.read_text(encoding="utf-8")

        # 2. 上传封面图（如果提供）
        thumb_media_id = None
        if cover_image and cover_image.exists():
            thumb_media_id = self.upload_image(cover_image)

        # 3. 创建草稿
        article_title = title or input_path.stem
        media_id = self.create_draft(
            title=article_title,
            content=content,
            thumb_media_id=thumb_media_id
        )

        # 4. 获取草稿详情
        draft = self.get_draft(media_id)

        return {
            "media_id": media_id,
            "title": article_title,
            "status": "draft",
            "url": f"https://mp.weixin.qq.com/s/{media_id}",
            "draft": draft
        }

def load_config(account: str = "main") -> WechatConfig:
    """加载配置"""

    # 尝试从环境变量加载
    appid = os.getenv(f"WECHAT_APPID_{account.upper()}", os.getenv("WECHAT_APPID"))
    appsecret = os.getenv(f"WECHAT_APPSECRET_{account.upper()}", os.getenv("WECHAT_APPSECRET"))

    if not appid or not appsecret:
        # 尝试从配置文件加载
        config_file = Path.home() / ".wechat" / "config.json"
        if config_file.exists():
            config_data = json.loads(config_file.read_text())
            account_config = config_data.get("accounts", {}).get(account, {})
            appid = account_config.get("appid")
            appsecret = account_config.get("appsecret")

    if not appid or not appsecret:
        raise ValueError(f"未找到账号 {account} 的配置，请设置环境变量或配置文件")

    return WechatConfig(appid=appid, appsecret=appsecret)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="公众号草稿发布工具")
    parser.add_argument("--input", "-i", required=True, help="输入 HTML 文件")
    parser.add_argument("--title", "-t", help="文章标题")
    parser.add_argument("--cover", "-c", help="封面图路径")
    parser.add_argument("--account", "-a", default="main", help="公众号账号")
    parser.add_argument("--test", action="store_true", help="测试 API 连接")

    args = parser.parse_args()

    try:
        # 加载配置
        config = load_config(args.account)

        # 创建发布器
        publisher = WechatPublisher(config)

        # 测试模式
        if args.test:
            token = publisher.get_access_token()
            print(f"✅ API 连接正常，Access Token: {token[:20]}...")
            return

        # 发布草稿
        result = publisher.publish(
            input_path=Path(args.input),
            title=args.title,
            cover_image=Path(args.cover) if args.cover else None
        )

        print(f"\n✅ 发布成功！")
        print(f"📄 标题: {result['title']}")
        print(f"🆔 Media ID: {result['media_id']}")
        print(f"🔗 链接: {result['url']}")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
