from Video import Video

print(Video.GetDownloadUrl(""));


for video in Video.GetVideos(""):
    print(video.ToMessage()+"\n");
