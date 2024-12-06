import base64
import os
from io import BytesIO
from PIL import Image
import asyncio
import aiohttp
import requests
from mimetypes import guess_type
from typing import Dict, List, Set, Optional


def encode_base64_from_local_path(file_path, return_with_mime=True):
    """
    Encode a local file to a Base64 string, with optional MIME type prefix.
    """
    mime_type, _ = guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"
    with open(file_path, "rb") as file:
        base64_data = base64.b64encode(file.read()).decode("utf-8")
        if return_with_mime:
            return f"data:{mime_type};base64,{base64_data}"
        return base64_data


async def encode_base64_from_url(url, session: aiohttp.ClientSession, return_with_mime=True):
    """
    Fetch a file from a URL and encode it to a Base64 string, with optional MIME type prefix.
    """
    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()
        mime_type = response.headers.get("Content-Type", "application/octet-stream")
        base64_data = base64.b64encode(content).decode("utf-8")
        if return_with_mime:
            return f"data:{mime_type};base64,{base64_data}"
        return base64_data


def encode_base64_from_pil(image: Image.Image, return_with_mime=True):
    """
    Encode a PIL image object to a Base64 string, with optional MIME type prefix.
    """
    buffer = BytesIO()
    image_format = image.format or "PNG"  # Default to PNG if format is unknown
    mime_type = f"image/{image_format.lower()}"
    image.save(buffer, format=image_format)
    buffer.seek(0)
    base64_data = base64.b64encode(buffer.read()).decode("utf-8")
    if return_with_mime:
        return f"data:{mime_type};base64,{base64_data}"
    return base64_data


async def encode_to_base64(file_source, session: aiohttp.ClientSession, return_with_mime=True):
    """
    A unified function to encode local files, URLs, or PIL images to Base64 strings,
    with optional MIME type prefix.
    """
    if isinstance(file_source, str):
        # Handle "file://" prefix for local paths
        if file_source.startswith("file://"):
            file_path = file_source[7:]  # Remove "file://"
            if os.path.exists(file_path):
                return encode_base64_from_local_path(file_path, return_with_mime)
            else:
                raise ValueError("Local file not found.")
        elif os.path.exists(file_source):
            # Local file path without "file://"
            return encode_base64_from_local_path(file_source, return_with_mime)
        elif file_source.startswith("http"):
            # URL - async fetch and encode
            return await encode_base64_from_url(file_source, session, return_with_mime)
        else:
            raise ValueError("Unsupported file source type.")
    elif isinstance(file_source, Image.Image):
        # PIL Image
        return encode_base64_from_pil(file_source, return_with_mime)
    else:
        raise ValueError("Unsupported file source type.")


# deprecated
def encode_base64_from_url_slow(url):
    response = requests.get(url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")


# deprecated
async def encode_image_to_base64(image_url, session):
    if isinstance(image_url, str):
        # 处理 "file://" 前缀的本地路径
        if image_url.startswith("file://"):
            file_path = image_url[7:]  # 去掉 "file://"
            if os.path.exists(file_path):
                return encode_base64_from_local_path(file_path)
            else:
                raise ValueError("本地文件未找到。")
        elif os.path.exists(image_url):
            # 本地文件路径，无需 "file://"
            return encode_base64_from_local_path(image_url)
        elif image_url.startswith("http"):
            # 网络 URL - 异步下载
            return await encode_base64_from_url(image_url, session)
        else:
            raise ValueError("不支持的图像来源类型。")
    elif isinstance(image_url, Image.Image):
        # PIL 图像
        return encode_base64_from_pil(image_url)
    else:
        raise ValueError("不支持的图像来源类型。")


def decode_base64_to_pil(base64_string):
    """将base64字符串解码为PIL Image对象"""
    try:
        # 如果base64字符串包含header (如 'data:image/jpeg;base64,')，去除它
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]

        # 解码base64为二进制数据
        image_data = base64.b64decode(base64_string)

        # 转换为PIL Image对象
        image = Image.open(BytesIO(image_data))
        return image
    except Exception as e:
        raise ValueError(f"无法将base64字符串解码为图像: {str(e)}")


def decode_base64_to_file(base64_string, output_path, format="JPEG"):
    """将base64字符串解码并保存为图片文件"""
    try:
        # 获取PIL Image对象
        image = decode_base64_to_pil(base64_string)

        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # 保存图像
        image.save(output_path, format=format)
        return True
    except Exception as e:
        raise ValueError(f"无法将base64字符串保存为文件: {str(e)}")


def decode_base64_to_bytes(base64_string):
    """将base64字符串解码为字节数据"""
    try:
        # 如果base64字符串包含header，去除它
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]

        # 解码为字节数据
        return base64.b64decode(base64_string)
    except Exception as e:
        raise ValueError(f"无法将base64字符串解码为字节数据: {str(e)}")


async def process_content_recursive(content, session):
    """
    Recursively process a content dictionary, replacing any URL with its Base64 equivalent.
    """
    if isinstance(content, dict):
        for key, value in content.items():
            if key == "url" and isinstance(value, str):  # Detect URL fields
                base64_data = await encode_to_base64(value, session)
                if base64_data:
                    content[key] = base64_data
            else:
                await process_content_recursive(value, session)
    elif isinstance(content, list):
        for item in content:
            await process_content_recursive(item, session)


async def messages_preprocess(messages):
    """
    Process a list of messages, converting URLs in any type of content to Base64.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [process_content_recursive(message, session) for message in messages]
        await asyncio.gather(*tasks)
    return messages


if __name__ == "__main__":
    from sparrow import relp
    # Example usage:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "请描述这几张图片"},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": f"{relp('./test_img.jpg')}"}},
            ],
        }
    ]
    from rich import print
    from sparrow import MeasureTime
    mt = MeasureTime()

    processed_messages = asyncio.run(messages_preprocess(messages))
    message = processed_messages[0]
    print(message)
    mt.show_interval()
