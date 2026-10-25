# Red-harvest

An extensible Python media downloader built on [yt-dlp](https://github.com/yt-dlp/yt-dlp), featuring a local web interface for downloading videos and audio, selecting video quality, downloading playlists, customizing output directories, and tracking download progress.

## Features

- [x] Download videos
- [x] Download audio (MP3)
- [x] Video quality selection
- [x] Playlist support
- [x] Custom download directory
- [x] Local web interface
- [x] Background downloads
- [x] Real-time download progress
- [ ] Advanced file naming options
- [ ] Interactive CLI
- [ ] Desktop GUI
- [ ] Configuration file
- [ ] Batch downloads
- [ ] Download queue and cancellation

## Technologies

- Python
- Flask
- yt-dlp
- FFmpeg
- HTML
- CSS
- JavaScript

## Requirements

- Python 3.10 or later
- FFmpeg installed and available on your system's PATH
- An internet connection for downloading media

## Installation

Clone the repository:

```bash
git clone https://github.com/Omarhagag27/Red-harvest.git
cd Red-harvest
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Install FFmpeg separately if it is not already installed.

## Usage

Start the application:

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

Enter a media URL, select the desired format and quality, configure the output directory if needed, and press **Download**.

Downloaded files are saved to the project's `downloads/` directory by default.

## Project Structure

```text
Red-harvest/
├── app.py
├── red_harvest/
│   └── downloader.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
├── downloads/
├── tests/
└── requirements.txt
```

- `app.py` — Flask application and HTTP endpoints.
- `red_harvest/downloader.py` — Download logic and progress reporting.
- `templates/index.html` — Web interface structure.
- `static/style.css` — Interface styling.
- `static/app.js` — Browser interactions and progress polling.
- `downloads/` — Default output directory.
- `tests/` — Automated tests (planned).

## Roadmap

- [x] Implement video downloading
- [x] Build a local web interface
- [x] Add audio extraction
- [x] Add video quality selection
- [x] Add playlist support
- [x] Support custom output directories
- [x] Implement background downloads
- [x] Add download progress tracking
- [ ] Improve file naming and organization
- [ ] Add automated tests
- [ ] Implement an interactive CLI
- [ ] Add a configuration file
- [ ] Support batch downloads
- [ ] Add download queue management and cancellation
- [ ] Improve error handling and download history

## License

MIT
