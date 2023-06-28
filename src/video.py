import os
from googleapiclient.discovery import build
from dotenv import load_dotenv


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
        self.video_id = video_id
        _video_info = self.get_info()
        self.title = _video_info["items"][0]["snippet"]["title"]
        self.url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.viewers = _video_info["items"][0]["statistics"]["viewCount"]
        self.likes = _video_info["items"][0]["statistics"]["likeCount"]

    def get_info(self) -> dict:
        return self.youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id