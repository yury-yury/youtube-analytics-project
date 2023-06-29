import datetime
import os
import isodate
from typing import List, Any, Dict
from googleapiclient.discovery import build
from dotenv import load_dotenv

from src.video import Video

load_dotenv()


# class PLVideo(Video):
#
#     def __init__(self, video_id: str, playlist_id: str) -> None:
#         super().__init__(video_id)
#         self.playlist_id = playlist_id


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.id = playlist_id
        self.title = self.get_info()['items'][0]['snippet']['localized']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.id}'
        self.video_ids = self.get_video_ids()

    def get_info(self) -> Dict[str, Any]:
        return self.youtube.playlists().list(part='snippet', id=self.id).execute()

    def get_video_ids(self) -> List[str]:
        videos = self.youtube.playlistItems().list(playlistId=self.id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        return [video['contentDetails']['videoId'] for video in videos['items']]

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for id in self.video_ids:
            video = Video(id)
            total_duration += video.duration
        return total_duration

    def show_best_video(self) -> str:
        best_likes = 0
        best_video = ''

        for video_id in self.video_ids:
            video = Video(video_id)
            if video.likes > best_likes:
                best_likes = video.likes
                best_video = video.url

        return best_video

