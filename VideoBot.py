from TelegramBot import TelegramBot
from TelegramClient import TelegramClient
from GifBuilder import GifBuilder
from Video import Video
from os.path import exists
import os


class VideoBot:
    DicUsers={};
    DicNombres={};
    def __init__(self,token,urlBase):
        self.Bot=TelegramBot(token);
        self.UrlBase=urlBase;
        self.Sitio=urlBase.split("/")[2];
    
    def Start(self):
        metodo=lambda cli:self._DoIt(cli);
        return self.Bot.Start(metodo);
    
    def _DoIt(self,telegramClient):
        try:
            if telegramClient.Nombre is not None:
                VideoBot.DicNombres[telegramClient.Id]=telegramClient.Nombre;
                telegramClient.SendText("Ahora te llamaré "+telegramClient.Nombre);
            elif telegramClient.GifOn is not None:
                if telegramClient.Id not in VideoBot.DicUsers or  VideoBot.DicUsers[telegramClient.Id]!=telegramClient.GifOn:
                    if telegramClient.GifOn:
                        telegramClient.SendText("Gif activados");
                    else:
                        telegramClient.SendText("Gif desactivados");

                VideoBot.DicUsers[telegramClient.Id]=telegramClient.GifOn;

            elif telegramClient.IsAnUrl is not None:
                if telegramClient.IsAnUrl:
                    if self.Sitio in telegramClient.MessageUrl:
                        result=Video.GetDownloadUrl(telegramClient.MessageUrl);
                        gifFile=None;
                        if telegramClient.Id in VideoBot.DicUsers and not VideoBot.DicUsers[telegramClient.Id]:
                            telegramClient.SendPhoto(result.Img,result.Url);
                        else:     
                            try:
                                gifFile=GifBuilder(result).GetGif(result.Title.replace(" ","_"));
                                telegramClient.SendAnimation(gifFile.Path,result.Url);
                            except:
                                telegramClient.SendPhoto(result.Img,result.Url);
                            finally:
                                if gifFile is not None and exists(gifFile.Path):
                                    os.remove(gifFile.Path);
                    else:
                        telegramClient.SendText("Link invalido, solo links a sitio oficial");
                else:
                    url=self.UrlBase+"&k="+telegramClient.MessageText;
                    total=0;
                    for video in Video.GetVideos(url):
                        total+=1;
                        try:
                            telegramClient.SendPhoto(video.Img,video.ToMessage());
                        except:
                            telegramClient.SendText(video.ToMessage());   
                    if total == 0:
                        if telegramClient.Id not in VideoBot.DicNombres:
                            telegramClient.SendText("No se ha encontrado ningun video!");
                        else:
                            telegramClient.SendText("No he encontrado nada "+str(VideoBot.DicNombres[telegramClient.Id])+"...");   
            else:
                telegramClient.SendText("/mejorFoto para desactivar los gif al enviar un link además de ir más rapida la respuesta");
                telegramClient.SendText("/mejorGif para activar los gif al enviar un link");
                telegramClient.SendText("/nombre para poner un poco de personalización");
                telegramClient.SendText("los comandos quizás se tienen que reenviar, eso pasa al reeiniciar el servidor ya que se guarda en memoria para mejor discreción.");
        except Exception as e:
            print("Ha habido un error "+str(e));
