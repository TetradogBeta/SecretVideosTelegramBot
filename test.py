from Video import Video
from GifBuilder import GifBuilder

print(Video.GetDownloadUrl("https://www.xvideos.com/video8706329/acariciando_resbaladizo_con_wiley"));


for video in Video.GetVideos("https://www.xvideos.com/?k=young&typef=gay"):
    #print(video.ToMessage()+"\n");
    print(GifBuilder(Video.GetDownloadUrl(video.Url)).GetGif(video.Title.replace(" ","_")));



