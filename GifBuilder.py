from PIL import Image
import urllib
import requests
import io

class GifBuilder:

    def __init__(self,objVideo,columnas=10,filas=10):#hay 10x10 imgs

        if isinstance(objVideo, bytearray):
            image_file = io.BytesIO(objVideo); 
        elif isinstance(objVideo, str):
            fd = urllib.request.urlopen(str(objVideo));
            image_file = io.BytesIO(fd.read());  
        else:
            fd = urllib.request.urlopen(objVideo.BigSlide);
            image_file = io.BytesIO(fd.read());

        self.Img= Image.open(image_file); 
        self.Fotogramas=None;
        self.Columnas=columnas;
        self.Filas=filas;

    def GetImgs(self):
        if self.Fotogramas is None:
            width=self.Img.size[0]/int(self.Columnas);
            height=self.Img.size[1]/int(self.Filas);

            for y in range(self.Filas):
                for x in range(self.Columnas):
                    caja = (x*width, y*height, (x*width) + width, (y*height) + height);
                    yield self.Img.crop(caja);
        else:
            for fotograma in self.Fotogramas:
                yield fotograma;

    def LoadFotogramas(self):
        if self.Fotogramas is None:
            fotogramas=[];
            for fotograma in self.GetImgs():
                fotogramas.append(fotograma);
            self.Fotogramas=fotogramas;

    def GetGif(self,fileNameWithOutExtension=None,duration=550):
        
        if fileNameWithOutExtension is None:
            fileNameWithOutExtension="imgGif";

        obj=lambda:None;    
        fileName=fileNameWithOutExtension+".gif";    
        self.LoadFotogramas();
        self.Fotogramas[0].save(fileName, format='GIF',
                        append_images=self.Fotogramas[1:], save_all=True, duration=duration, loop=0);
        obj.Path=fileName;
        obj.Duration=duration;
        obj.Width=self.Fotogramas[0].size[0];
        obj.Height=self.Fotogramas[0].size[1];
        return obj;



    
