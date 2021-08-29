from Video import Video
from GifBuilder import GifBuilder

print(Video.GetDownloadUrl(""));


for video in Video.GetVideos(""):
    print(video.ToMessage()+"\n");
    
