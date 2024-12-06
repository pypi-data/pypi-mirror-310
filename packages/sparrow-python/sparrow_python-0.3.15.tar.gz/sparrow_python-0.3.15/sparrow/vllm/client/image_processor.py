import base64
import os
from io import BytesIO
from PIL import Image
import asyncio
import aiohttp
import requests
from typing import Dict, List, Set, Optional


def encode_base64_from_local_path(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


async def encode_base64_from_url(url, session: aiohttp.ClientSession):
    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()
        return base64.b64encode(content).decode("utf-8")

def encode_base64_from_url_slow(url):
    response = requests.get(url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")

def encode_base64_from_pil(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


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


# async def messages_preprocess(messages: list[dict]):
#     async def process_image_content(content, session):
#         image_url = content["image_url"].get("url")
#         image_base64 = await encode_image_to_base64(image_url, session)
#         content["image_url"]["url"] = f"data:image/jpeg;base64,{image_base64}"
#
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#
#         for message in messages:
#             if message["role"] == "user" and "content" in message:
#                 for content in message["content"]:
#                     if content.get("type") == "image_url":
#                         tasks.append(process_image_content(content, session))
#
#         # Concurrently process all image URLs
#         await asyncio.gather(*tasks)
#
#     return messages


class MessagePreprocessor:
    def __init__(self, media_types: Optional[Set[str]] = None):
        """
        初始化消息预处理器
        :param media_types: 需要处理的媒体类型集合，例如 {"image_url", "image", "video_url"}
        """
        # 如果没有指定媒体类型，使用默认值
        self.media_types = media_types or {"image_url", "image"}

    async def encode_to_base64(self, url: str, session: aiohttp.ClientSession) -> str:
        """将URL指向的媒体内容转换为base64编码"""
        if url.startswith("file://"):
            file_path = url[7:]
            with open(file_path, "rb") as file:
                return base64.b64encode(file.read()).decode("utf-8")
        elif os.path.exists(url):
            with open(url, "rb") as file:
                return base64.b64encode(file.read()).decode("utf-8")
        else:
            async with session.get(url) as response:
                response.raise_for_status()
                content = await response.read()
                return base64.b64encode(content).decode("utf-8")

    async def process_content(self, content: Dict, session: aiohttp.ClientSession) -> None:
        """处理单个内容项"""
        try:
            # 获取URL - 支持多种格式
            url = (content.get("image_url", {}).get("url") or  # {"image_url": {"url": "..."}}
                   content.get("image_url") or  # {"image_url": "..."}
                   content.get("image") or  # {"image": "..."}
                   content.get("video_url", {}).get("url") or  # {"video_url": {"url": "..."}}
                   content.get("video_url") or  # {"video_url": "..."}
                   content.get("url"))  # {"url": "..."}

            if not url:
                return

            # 转换为base64
            base64_data = await encode_image_to_base64(url, session)

            # 更新内容 - 保持原有格式
            if "image_url" in content and isinstance(content["image_url"], dict):
                content["image_url"]["url"] = f"data:image/jpeg;base64,{base64_data}"
            elif "image_url" in content:
                content["image_url"] = f"data:image/jpeg;base64,{base64_data}"
            elif "image" in content:
                content["image"] = f"data:image/jpeg;base64,{base64_data}"
            elif "video_url" in content and isinstance(content["video_url"], dict):
                content["video_url"]["url"] = f"data:video/mp4;base64,{base64_data}"
            elif "video_url" in content:
                content["video_url"] = f"data:video/mp4;base64,{base64_data}"
            elif "url" in content:
                content["url"] = f"data:image/jpeg;base64,{base64_data}"

        except Exception as e:
            print(f"处理内容时发生错误: {str(e)}")

    async def process_messages(self, messages: List[Dict]) -> List[Dict]:
        """
        处理消息列表中的所有媒体URL
        :param messages: 消息列表
        :return: 处理后的消息列表
        """
        async with aiohttp.ClientSession() as session:
            tasks = []

            for message in messages:
                if message["role"] == "user" and "content" in message:
                    for content in message["content"]:
                        if (isinstance(content, dict) and
                                content.get("type") in self.media_types):
                            tasks.append(self.process_content(content, session))

            if tasks:
                await asyncio.gather(*tasks)

            return messages

async def messages_preprocess(messages: list[dict]):
    preprocessor = MessagePreprocessor()
    processed_messages = await preprocessor.process_messages(messages)
    return processed_messages


# class ContentType(Enum):
#     """内容类型枚举"""
#     IMAGE = auto()
#     VIDEO = auto()
#     AUDIO = auto()
#     TEXT = auto()
#
#     @classmethod
#     def from_type_str(cls, type_str: str) -> Optional['ContentType']:
#         """从字符串推断内容类型"""
#         type_mapping = {
#             'image': cls.IMAGE,
#             'image_url': cls.IMAGE,
#             'video': cls.VIDEO,
#             'video_url': cls.VIDEO,
#             'audio': cls.AUDIO,
#             'audio_url': cls.AUDIO,
#             'text': cls.TEXT
#         }
#         return type_mapping.get(type_str.lower())
#
#
# @dataclass
# class ProcessingResult:
#     """处理结果数据类"""
#     success: bool
#     content: Dict
#     error: Optional[str] = None
#
#
# class ContentProcessor(ABC):
#     """内容处理器抽象基类"""
#
#     @abstractmethod
#     async def process(self, content: Dict, session: aiohttp.ClientSession) -> ProcessingResult:
#         """处理单个内容项"""
#         pass
#
#     @abstractmethod
#     def can_process(self, content: Dict) -> bool:
#         """判断是否可以处理该内容"""
#         pass
#
#
# class MediaProcessor(ContentProcessor):
#     """媒体处理器基类"""
#
#     def __init__(self, content_type: ContentType):
#         self.content_type = content_type
#         self.url_keys = {'url', 'image_url', 'video_url', 'audio_url', 'image', 'video', 'audio'}
#
#     def can_process(self, content: Dict) -> bool:
#         # 检查内容类型
#         if 'type' in content:
#             content_type = ContentType.from_type_str(content['type'])
#             if content_type != self.content_type:
#                 return False
#
#         # 检查是否包含可处理的URL键
#         return any(self._find_url_key(content))
#
#     def _find_url_key(self, obj: Union[Dict, Any]) -> List[str]:
#         """递归查找所有URL键"""
#         found_keys = []
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 if key in self.url_keys:
#                     found_keys.append(key)
#                 if isinstance(value, (dict, list)):
#                     found_keys.extend(self._find_url_key(value))
#         elif isinstance(obj, list):
#             for item in obj:
#                 found_keys.extend(self._find_url_key(item))
#         return found_keys
#
#     def _extract_url(self, content: Dict) -> Optional[str]:
#         """从内容中提取URL"""
#         for key in self._find_url_key(content):
#             value = content
#             for k in key.split('.'):
#                 if isinstance(value, dict):
#                     value = value.get(k)
#                 else:
#                     value = None
#                     break
#             if isinstance(value, str):
#                 return value
#             elif isinstance(value, dict) and 'url' in value:
#                 return value['url']
#         return None
#
#     def _update_url(self, content: Dict, new_url: str) -> Dict:
#         """更新内容中的URL"""
#         new_content = content.copy()
#         for key in self._find_url_key(content):
#             value = content
#             path = key.split('.')
#             for k in path[:-1]:
#                 value = value[k]
#             if isinstance(value[path[-1]], str):
#                 value[path[-1]] = new_url
#             elif isinstance(value[path[-1]], dict):
#                 value[path[-1]]['url'] = new_url
#         return new_content
#
#
# class ImageProcessor(MediaProcessor):
#     """图片处理器"""
#
#     def __init__(self):
#         super().__init__(ContentType.IMAGE)
#
#     async def process(self, content: Dict, session: aiohttp.ClientSession) -> ProcessingResult:
#         try:
#             url = self._extract_url(content)
#             if not url:
#                 return ProcessingResult(False, content, "未找到图片URL")
#
#             base64_data = await self._encode_image_to_base64(url, session)
#             base64_url = f"data:image/jpeg;base64,{base64_data}"
#             new_content = self._update_url(content, base64_url)
#
#             return ProcessingResult(True, new_content)
#
#         except Exception as e:
#             return ProcessingResult(False, content, str(e))
#
#     async def _encode_image_to_base64(self, image_source: Union[str, Image.Image],
#                                       session: aiohttp.ClientSession) -> str:
#         """将图片转换为base64编码"""
#         if isinstance(image_source, str):
#             if image_source.startswith("file://"):
#                 file_path = image_source[7:]
#                 if os.path.exists(file_path):
#                     return self._encode_from_local_path(file_path)
#                 raise ValueError(f"本地文件未找到: {file_path}")
#
#             elif os.path.exists(image_source):
#                 return self._encode_from_local_path(image_source)
#
#             elif image_source.startswith(("http://", "https://")):
#                 return await self._encode_from_url(image_source, session)
#
#             raise ValueError(f"不支持的图像来源类型: {image_source}")
#
#         elif isinstance(image_source, Image.Image):
#             return self._encode_from_pil(image_source)
#
#         raise ValueError(f"不支持的图像来源类型: {type(image_source)}")
#
#     def _encode_from_local_path(self, file_path: str) -> str:
#         with open(file_path, "rb") as file:
#             return base64.b64encode(file.read()).decode("utf-8")
#
#     async def _encode_from_url(self, url: str, session: aiohttp.ClientSession) -> str:
#         async with session.get(url) as response:
#             response.raise_for_status()
#             content = await response.read()
#             return base64.b64encode(content).decode("utf-8")
#
#     def _encode_from_pil(self, image: Image.Image) -> str:
#         buffered = BytesIO()
#         image.save(buffered, format="JPEG")
#         return base64.b64encode(buffered.getvalue()).decode("utf-8")
#
#
# class MessagePreprocessor:
#     """消息预处理器"""
#
#     def __init__(self):
#         self.processors: List[ContentProcessor] = [
#             ImageProcessor(),  # 可以在这里添加其他处理器
#         ]
#
#     def _get_processor(self, content: Dict) -> Optional[ContentProcessor]:
#         """获取适合处理该内容的处理器"""
#         for processor in self.processors:
#             if processor.can_process(content):
#                 return processor
#         return None
#
#     async def preprocess(self, messages: List[Dict]) -> List[Dict]:
#         """预处理消息列表"""
#         async with aiohttp.ClientSession() as session:
#             tasks = []
#             new_messages = []
#
#             for message in messages:
#                 new_message = message.copy()
#
#                 if message.get("role") == "user" and "content" in message:
#                     if isinstance(message["content"], list):
#                         new_content = []
#                         for content in message["content"]:
#                             processor = self._get_processor(content)
#                             if processor:
#                                 task = asyncio.create_task(processor.process(content, session))
#                                 tasks.append(task)
#                                 new_content.append(task)
#                             else:
#                                 new_content.append(content)
#
#                         if tasks:
#                             results = await asyncio.gather(*tasks)
#                             new_message["content"] = [
#                                 result.content if isinstance(item, asyncio.Task) else item
#                                 for item, result in zip(new_content, results)
#                             ]
#                         else:
#                             new_message["content"] = new_content
#
#                 new_messages.append(new_message)
#
#             return new_messages


# async def messages_preprocess(messages: List[Dict]) -> List[Dict]:
#     print('llala')
#     processor = MessagePreprocessor()
#     return await processor.preprocess(messages)

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
