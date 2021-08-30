import telepot
import urllib.parse
import os


class TelegramClient:
    ComandosTelegram=["/start"];
    ComandosGif=["/mejorfoto","/mejorgif"];
    ComandoNombre="/nombre";
    def __init__(self,bot,msg):
        self.GifOn=None;
        self.Nombre=None;
        #puede ser para buscar o para obtener el link(ya sea un link como text o contestan a un mensaje enviado)
        content_type, chat_type, chat_id = telepot.glance(msg);
        self.ChatId=chat_id;
        self.Bot=bot;
        self.Message=msg;
        self.Id=msg["chat"]["id"];
        #mirar si reenvian un video para obtener su link de descarga
        if  "text" in msg and "http" not in msg["text"] and "reply_to_message" not in msg:
            self._setText(msg["text"]);
        else:
            self.IsAnUrl=True;
            if "reply_to_message" in msg:
                self._setUrl(msg["reply_to_message"]["text"]); 
            
            elif "caption" in msg:
                self._setUrl(msg["caption"]);
            elif "text" in msg:#enviaron una url
                self._setUrl(msg["text"]);
                    
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
        textoOri=texto;
        texto=str(texto).lower();
        if TelegramClient.NoEsUnComando(texto):
            if " pagina " in texto:
                        campos=texto.split(" pagina ");
                        texto=campos[0];
                        pagina=campos[1].replace(" ","");
            else:
                pagina="1";    
            self.MessageText=urllib.parse.quote(texto)+"&p="+pagina;
            self.IsAnUrl=False;
        else:
            self.IsAnUrl=None;
            if texto in TelegramClient.ComandosGif:
                self.GifOn=texto==TelegramClient.ComandosGif[1];
            if TelegramClient.ComandoNombre in texto:
                if " " in textoOri:
                    self.Nombre=textoOri.replace(textoOri.split(" ")[0],"");
                else:    
                    self.Nombre=texto.replace(TelegramClient.ComandoNombre,"");
                    if len(self.Nombre)>1:
                        self.Nombre=self.Nombre[0].upper()+self.Nombre[1:].lower();
                    elif len(self.Nombre)==1:
                        self.Nombre=self.Nombre.upper();
                    else:
                        self.Nombre="";        

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

    @staticmethod
    def NoEsUnComando(texto):
        noEsComando= TelegramClient.ComandoNombre not in texto;
        if noEsComando:
            noEsComando= texto not in TelegramClient.ComandosGif;
            if noEsComando:
                noEsComando=texto not in TelegramClient.ComandosTelegram;
        return noEsComando;     
    
