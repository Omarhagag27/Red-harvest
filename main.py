import yt_dlp

url = input("Video URL: ")

opts = {
    "outtmpl": "%(title)s.%(ext)s",
}

with yt_dlp.YoutubeDL(opts) as ydl:
    ydl.download([url])