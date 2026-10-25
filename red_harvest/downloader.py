
# red_harvest/downloader.py

from pathlib import Path
from collections.abc import Callable

import yt_dlp


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOWNLOAD_DIR = PROJECT_ROOT / "downloads"


def download_media(
    url: str,
    media_type: str = "video",
    quality: str = "best",
    download_dir: str | None = None,
    playlist: bool = False,
    progress_callback: Callable[[dict], None] | None = None,
):
    if not url.strip():
        raise ValueError("Please provide a URL.")

    if media_type not in {"video", "audio"}:
        raise ValueError("Invalid media type.")

    quality_formats = {
        "best": "bestvideo*+bestaudio/best",
        "1080": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "720": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "480": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "360": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    }

    if quality not in quality_formats:
        raise ValueError("Unsupported video quality.")

    output_dir = (
        Path(download_dir).expanduser().resolve()
        if download_dir
        else DEFAULT_DOWNLOAD_DIR
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    def report(info):
        if progress_callback:
            progress_callback(info)

    def progress_hook(data):
        status = data.get("status")

        if status == "downloading":
            downloaded = data.get("downloaded_bytes", 0)
            total = (
                data.get("total_bytes")
                or data.get("total_bytes_estimate")
            )

            percent = downloaded / total * 100 if total else None

            report({
                "status": "downloading",
                "percent": round(percent, 1) if percent is not None else None,
                "downloaded_bytes": downloaded,
                "total_bytes": total,
                "speed": data.get("speed"),
                "eta": data.get("eta"),
                "filename": Path(
                    data.get("filename", "")
                ).name,
            })

        elif status == "finished":
            report({
                "status": "processing",
                "percent": 100,
                "filename": Path(
                    data.get("filename", "")
                ).name,
            })

    options = {
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "noplaylist": not playlist,
        "format": (
            "bestaudio/best"
            if media_type == "audio"
            else quality_formats[quality]
        ),
        "quiet": True,
        "no_warnings": True,
        "windowsfilenames": True,
        "progress_hooks": [progress_hook],
    }

    if media_type == "audio":
        options["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        options["merge_output_format"] = "mp4"

    try:
        report({"status": "starting", "percent": 0})

        with yt_dlp.YoutubeDL(options) as downloader:
            result = downloader.extract_info(url, download=True)

        title = result.get("title", "Download complete")

        report({
            "status": "completed",
            "percent": 100,
            "title": title,
        })

        return {
            "success": True,
            "title": title,
            "download_dir": str(output_dir),
        }

    except yt_dlp.utils.DownloadError as error:
        raise RuntimeError(f"Download failed: {error}") from error
