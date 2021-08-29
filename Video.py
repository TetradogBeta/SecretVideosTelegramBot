from bs4 import BeautifulSoup
from urllib.parse import urlparse
import cloudscraper
import re

class Video:
    def __init__(self,baseUrl,node):
        video=BeautifulSoup(str(node),"html.parser");
        videoLink=video.find_all("a")[1];
        self.BaseUrl=baseUrl;
        self.UrlRel=videoLink["href"];
        self.Img=video.find_all("img")[0]["data-src"];
        self.Title=videoLink["title"];
        self.Duration=video.find_all("span","duration")[0].text;
        self.Url=self.BaseUrl+self.UrlRel;

    def ToMessage(self):
        return self.Title+": "+self.Duration+"\n"+self.Url;
    
    @staticmethod
    def GetVideos(url):
        scraper = cloudscraper.create_scraper();
        page = scraper.get(url).text;
        soup = BeautifulSoup(page, "html.parser");
        baseUrl='{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url));
        for videoStr in soup.find_all("div","thumb-block"):
            yield Video(baseUrl,videoStr);

    @staticmethod
    def GetDownloadUrl(urlVideo):
        scraper = cloudscraper.create_scraper();
        page = scraper.get(urlVideo).text;
        obj = lambda: None;

        campos=page.split("html5player.setVideoUrlHigh('")[1].split("');");
        urlDownload= campos[0];
        campos=page.split("html5player.setThumbUrl('")[1].split("');");
        imgVideo=campos[0];
        campos=page.split("html5player.setThumbSlideBig('")[1].split("');");
        imgSlideBig=campos[0];
        campos=page.split("html5player.setVideoTitle('")[1].split("');");
        title=campos[0];

        obj.Url=urlDownload;
        obj.Img=imgVideo;
        obj.BigSlide=imgSlideBig;
        obj.Title=title;

        return obj;
