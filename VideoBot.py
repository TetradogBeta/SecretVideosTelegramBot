from TelegramBot import TelegramBot
from TelegramClient import TelegramClient
from GifBuilder import GifBuilder
from Video import Video

import os

class VideoBot:

    def __init__(self,token,urlBase):
        self.Bot=TelegramBot(token);
        self.UrlBase=urlBase;
    
    def Start(self):
        metodo=lambda cli:self._DoIt(cli);
        return self.Bot.Start(metodo);
    
    def _DoIt(self,telegramClient):
        if telegramClient.IsAnUrl:
            result=Video.GetDownloadUrl(telegramClient.MessageUrl);
            gifFile=GifBuilder(result).GetGif(result.Title.replace(" ","_"));
            telegramClient.SendAnimation(gifFile.Path,result.Url);
            os.remove(gifFile.Path);
        else:
            url=self.UrlBase+"&k="+telegramClient.MessageText;
            for video in Video.GetVideos(url):
                try:
                    telegramClient.SendPhoto(video.Img,video.ToMessage());
                except:
                    telegramClient.SendText(video.ToMessage());   
        
