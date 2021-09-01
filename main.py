from TelegramHelper.Bot import Bot
from TelegramHelper.DicMetodo import DicMetodo

from Video import Video
from GifBuilder import GifBuilder

from os.path import exists

import urllib.request
import os
import sys

def Main():
    fileConfig="Config";
    dicNombres={};
    dicLinkSettings={};
    if exists(fileConfig):
        fConfig = open(fileConfig, "r");
        config = fConfig.readlines();
        fConfig.close();
        token=config[0].replace("\n","");
        urlBase=config[1].replace("\n","");
        filtro=config[2].replace("\n","");
    elif len(sys.argv)>1:
        token=sys.argv[1];
        urlBase=sys.argv[2];
        filtro=sys.argv[3];
        fConfig = open(fileConfig, 'w');
        fConfig.writelines([token,urlBase,filtro]);
        fConfig.close();

    commands=["Start","Download","MejorFoto","MejorGif","Nombre"];
    bot=Bot(token,urlBase+" Videos V4.0");

    bot.AddCommand(commands[0], lambda cli,args:cli.SendText("1-Texto a buscar\n2-/"+commands[1]+" url (from "+urlBase+") si acaba en pagina x donde x es el numero de la pagina a continuar la busqueda\n3-/"+commands[2]+" para enviar más rápido el link enviando una foto\n4-/"+commands[3]+" para enviar un gif del slide del video\n5-/"+commands[4]+" para poderte dicir que no hay mensajes de una forma más personal xD\nTodos los comandos se guardan en la RAM así que no hay rastro si se reinicia el servidor por lo tanto puede ser que se tenga que configurar de vez en cuando."));

    dicMetodo=DicMetodo();
    dicMetodo.AddStarts(urlBase,SendVideo);
    bot.AddCommandPlus(commands[1], dicMetodo);

    bot.AddCommand(commands[2], lambda cli,args:SetSettings(cli,dicLinkSettings,False));
    bot.AddCommand(commands[3], lambda cli,args:SetSettings(cli,dicLinkSettings,True));
    bot.AddCommand(commands[4], lambda cli,args:SetName(cli,dicNombres));

    bot.Default.AddStarts(urlBase,lambda cli: SendUrlVideo(cli,dicLinkSettings,urlBase));
    bot.Default.AddStarts("http", lambda cli:cli.SendText("solo links de "+urlBase));
    bot.Default.AddContains(urlBase,lambda cli:LimpiaUrlYEnvia(cli,dicLinkSettings));
    bot.Default.Default=lambda cli:BuscaEnLaWeb(cli,urlBase+filtro,dicNombres);
    bot.ReplyTractament=ReplyTractament;
    bot.Start();

def ReplyTractament(cli):
    if cli.IsAReplyFromBot:
        cli.Args=cli.Reply.split("\n");
        if len(cli.Args)>0 and cli.Args[0].startswith("/"):
            cli.Command=str(cli.Args[0][1:]).lower();
            cli.Args=cli.Args[1:];

def LimpiaUrlYEnvia(cli,dicLinkSettings):
    text=" ".join(cli.Args);
    if "\n" in text:
        url=text.split("\n")[-1];
    elif cli.Args[-1].startswith("http"):
        url=cli.Args[-1];
    else:
        url=None;

    SendLink(cli, url, dicLinkSettings);
    
def SetName(cli,dicNombres):
    if cli.Args is None or len(cli.Args)==0:
        dicNombres[cli.Id]=None;
        cli.SendText("Nombre eliminado");
    else:
        dicNombres[cli.Id]=" ".join(cli.Args);
        cli.SendText("Ahora te llamaré '"+dicNombres[cli.Id]+"'");

def SetSettings(cli,dicLinkSettings,isGifOn):
    dicLinkSettings[cli.Id]=isGifOn;
    if isGifOn:
        cli.SendText("Gif activado");
    else:
        cli.SendText("Gif desactivado");

def SendVideo(cli):
    result=Video.GetDownloadUrl(cli.Args[0]);
    fileName=result.Title.replace(" ","_")+'.mp4';
    urllib.request.urlretrieve(result.Url, fileName);
    cli.SendVideo(fileName);
    os.remove(fileName); 

def SendUrlVideo(cli,dicLinkSettings,urlBase):
    url=None;
    if cli.IsAReply:
        if urlBase in cli.Reply:
            if "\n" in cli.Reply:
                url=cli.Reply.split("\n")[-1];
            else:
                url=cli.Reply;
    else:
        url=cli.Args[0];
    SendLink(cli,url,dicLinkSettings);

def SendLink(cli,url,dicLinkSettings):
    if url is not None:
        try:
            result=Video.GetDownloadUrl(url);
            if cli.Id not in dicLinkSettings or not dicLinkSettings[cli.Id]:
                cli.SendPhoto(result.Img,result.Url);
            else:
                gifFile=GifBuilder(result).GetGif(result.Title.replace(" ","_"));
                cli.SendVideo(gifFile.Path,result.Url);
                os.remove(gifFile.Path);
        except:
            cli.SendText("Error con el link enviado!!");


def BuscaEnLaWeb(cli,urlBaseConFiltro,dicNombres):

    texto=" ".join(cli.Args);
    if " pagina " in texto:
                        campos=texto.split(" pagina ");
                        texto=campos[0];
                        pagina=campos[1].replace(" ","");
    else:
        pagina="1";

    texto=urllib.parse.quote(texto)+"&p="+pagina;
    url=urlBaseConFiltro+"&k="+texto;
    total=0;
    for video in Video.GetVideos(url):
        total+=1;
        try:
            cli.SendPhoto(video.Img,video.ToMessage());
        except:
            cli.SendText(video.ToMessage());   
    if total == 0:
        if cli.Id not in dicNombres or dicNombres[cli.Id] is None:
            cli.SendText("No se ha encontrado ningun video!");
        else:
            cli.SendText("No he encontrado nada "+str(dicNombres[cli.Id])+"...");  



Main();