
# app.py

from threading import Thread, Lock
from uuid import uuid4
from urllib.parse import urlparse

from flask import Flask, render_template, request, jsonify

from red_harvest.downloader import download_media

app = Flask(__name__)

jobs = {}
jobs_lock = Lock()


def update_job(job_id, info):
    with jobs_lock:
        if job_id in jobs:
            jobs[job_id].update(info)


def run_download(job_id, options):
    try:
        result = download_media(
            **options,
            progress_callback=lambda info: update_job(job_id, info),
        )

        update_job(job_id, {
            "status": "completed",
            "percent": 100,
            "result": result,
        })

    except Exception as error:
        app.logger.exception("Download job %s failed", job_id)

        update_job(job_id, {
            "status": "failed",
            "error": str(error),
        })


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json(silent=True) or {}

    url = data.get("url", "").strip()
    media_type = data.get("media_type", "video")
    quality = data.get("quality", "best")
    download_dir = data.get("download_dir") or None
    playlist = data.get("playlist", False)

    parsed_url = urlparse(url)

    if (
        parsed_url.scheme not in {"http", "https"}
        or not parsed_url.netloc
    ):
        return jsonify(error="Please enter a valid HTTP or HTTPS URL."), 400

    if media_type not in {"video", "audio"}:
        return jsonify(error="Invalid media type."), 400

    if quality not in {"best", "1080", "720", "480", "360"}:
        return jsonify(error="Invalid video quality."), 400

    if not isinstance(playlist, bool):
        return jsonify(error="Playlist must be true or false."), 400

    job_id = str(uuid4())

    options = {
        "url": url,
        "media_type": media_type,
        "quality": quality,
        "download_dir": download_dir,
        "playlist": playlist,
    }

    with jobs_lock:
        jobs[job_id] = {
            "status": "starting",
            "percent": 0,
        }

    thread = Thread(
        target=run_download,
        args=(job_id, options),
        daemon=True,
    )
    thread.start()

    return jsonify(job_id=job_id), 202


@app.route("/progress/<job_id>", methods=["GET"])
def get_progress(job_id):
    with jobs_lock:
        job = jobs.get(job_id)

        if job is None:
            return jsonify(error="Download job not found."), 404

        return jsonify(job)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
