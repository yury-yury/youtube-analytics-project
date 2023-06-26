import json
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv


load_dotenv()


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
            id канала
            название канала
            описание канала
            ссылка на канал
            количество подписчиков
            количество видео
            общее количество просмотров
"""
        self.__channel_id: str = channel_id
        _channel_info = self.get_info()
        self.title = _channel_info["items"][0]["snippet"]["title"]
        self.description = _channel_info["items"][0]["snippet"]["description"]
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber = _channel_info["items"][0]["statistics"]["subscriberCount"]
        self.video_count = _channel_info["items"][0]["statistics"]["videoCount"]
        self.viewers = _channel_info["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_info()
        printj(channel)

    def get_info(self) -> dict:
        return self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    def to_json(self, filename):
        channel_dict = {"id": self.channel_id,
                        "title": self.title,
                        "video_count": self.video_count,
                        "url": self.url,
                        "description": self.description
                        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_dict, file, indent=2, ensure_ascii=False)


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
