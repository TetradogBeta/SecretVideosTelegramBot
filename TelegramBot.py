from telepot.loop import MessageLoop
from TelegramClient import TelegramClient
import telepot

class TelegramBot:

    def __init__(self,token):
        self.Bot=telepot.Bot(token);
    
    def Start(self,method):
        metodo=lambda msg:method(self._ToTelegramClient(msg));
        return MessageLoop(self.Bot, handle=metodo);
    
    def _ToTelegramClient(self,message):
        return TelegramClient(self.Bot,message);

