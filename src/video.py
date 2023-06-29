import os
from datetime import datetime
from typing import Dict, Any

import isodate
from googleapiclient.discovery import build
from dotenv import load_dotenv

from src.channel import printj

load_dotenv()


class Video:
    """
    Реализуйте инициализацию реальными данными следующих атрибутов экземпляра класса `Video`:
  - id видео
  - название видео
  - ссылка на видео
  - количество просмотров
  - количество лайков
    """
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id: str = video_id
        _video_info: Dict[str, Any] = self.get_info()
        self.title: str = _video_info["items"][0]["snippet"]["title"]
        self.url: str = f'https://youtu.be/{self.video_id}'
        self.viewers: int = int(_video_info["items"][0]["statistics"]["viewCount"])
        self.likes: int = int(_video_info["items"][0]["statistics"]["likeCount"])
        self.duration: datetime = isodate.parse_duration(_video_info['items'][0]['contentDetails']['duration'])

    def get_info(self) -> dict:
        return self.youtube.videos().list(id=self.video_id, part='contentDetails,snippet,statistics').execute()

    def __str__(self):
        return f"{self.title}"
