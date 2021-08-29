import telepot
import urllib.parse
import os


class TelegramClient:
    def __init__(self,bot,msg):
        #puede ser para buscar o para obtener el link(ya sea un link como text o contestan a un mensaje enviado)
        content_type, chat_type, chat_id = telepot.glance(msg);
        self.ChatId=chat_id;
        self.Bot=bot;
        self.Message=msg;
        #mirar si reenvian un video para obtener su link de descarga
        if  "text" in msg and "http" not in msg["text"]:
            self._setText(msg["text"]);
        else:
            self.IsAnUrl=True;
            if "text" in msg:#enviaron una url
                self.MessageUrl=msg["text"];
            elif "caption" in msg:
                self._setUrl(msg["caption"]);#se que no es este...necesito saber como viene
            elif "reply_to_message" in msg:
                self._setUrl(message["reply_to_message"]["caption"]);
                    
    def _setUrl(self,message):
        if "http" in message:
            if "\n" in message:
                camposUrl=message.split("\n");
                self.MessageUrl=camposUrl[-1];
            else:
                self.MessageUrl=message; 
        else:
            self._setText(message);
    def _setText(self,texto):
        texto=str(texto).lower();
        if " pagina " in texto:
                    campos=texto.split(" pagina ");
                    texto=campos[0];
                    pagina=campos[1].replace(" ","");
        else:
            pagina="1";    
        self.MessageText=urllib.parse.quote(texto)+"&p="+pagina;
        self.IsAnUrl=False;

    def SendPhoto(self,urlImg,desc=""):
        self.Bot.sendPhoto(self.ChatId,urlImg,desc);

    def SendText(self,text):
        self.Bot.sendMessage(self.ChatId,text);
    
    def SendVideo(self,pathVideo,desc=""):
        stream=open(pathVideo,"rb");
        self.Bot.sendVideo(self.ChatId,stream,caption=desc);
        stream.close();

    def SendAnimation(self,pathAnimation,desc=""):
        self.SendVideo(pathAnimation,desc);
    
