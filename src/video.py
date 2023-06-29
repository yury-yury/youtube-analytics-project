import os
from datetime import datetime
from typing import Dict, Any, Optional
# from googleapiclient.errors import HttpError
import isodate
from googleapiclient.discovery import build
from dotenv import load_dotenv

from src.channel import printj

load_dotenv()


class HttpError(Exception):
    pass


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
        try:
            _video_info: Dict[str, Any] = self.get_info()
        except HttpError:
            self.title: Optional[str] = None
            self.url: Optional[str] = None
            self.viewers: Optional[int] = None
            self.like_count: Optional[int] = None
            self.duration: Optional[datetime] = None
        else:
            self.title: Optional[str] = _video_info["items"][0]["snippet"]["title"]
            self.url: Optional[str] = f'https://youtu.be/{self.video_id}'
            self.viewers: Optional[int] = int(_video_info["items"][0]["statistics"]["viewCount"])
            self.like_count: Optional[int] = int(_video_info["items"][0]["statistics"]["likeCount"])
            self.duration: Optional[datetime] = isodate.parse_duration(_video_info['items'][0]['contentDetails']['duration'])

    def get_info(self) -> dict:
        response = self.youtube.videos().list(id=self.video_id, part='contentDetails,snippet,statistics').execute()
        if len(response['items']) == 0:
            raise HttpError
        return response

    def __str__(self):
        return f"{self.title}"
