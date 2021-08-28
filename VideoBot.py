from TelegramBot import TelegramBot
from TelegramClient import TelegramClient
from Video import Video

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
            telegramClient.SendPhoto(result.Img,result.Url);
        else:
            url=self.UrlBase+"&k="+telegramClient.MessageText;
            for video in Video.GetVideos(url):
                try:
                    telegramClient.SendPhoto(video.Img,video.ToMessage());
                except:
                    telegramClient.SendText(video.ToMessage());   
        
