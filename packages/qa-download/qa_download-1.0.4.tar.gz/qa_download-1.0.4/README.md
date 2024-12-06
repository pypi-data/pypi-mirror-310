Here's the updated `README.md` with samples for downloading using a YouTube URL, along with a note recommending using the song name for better metadata matching:

---

# Music Downloader 🎶

**Music Downloader** is a Python tool that downloads music from YouTube and automatically embeds metadata, album artwork, and lyrics from Genius. Perfect for building your offline music library with well-organized tags and rich media.

## Features

- **Downloads audio** from YouTube as MP3
- **Embeds metadata** like title, artist, album, and release date
- **Fetches album artwork** and attaches it to the MP3
- **Adds lyrics** automatically from Genius
- Works with most Python environments and media players

## Installation

You can install Music Downloader via the `qa-download` package from PyPI:

```bash
pip install qa-download
```

## Requirements

- Python 3.7 or higher
- YouTube audio extraction and metadata libraries (automatically installed with the package)

## Usage

Once installed, use `music-downloader` directly from the command line.

**Recommended:** Using the song title (instead of a YouTube URL) gives more accurate metadata from Genius.

### Downloading by Song Name

Using a song title helps **Music Downloader** find better metadata, artwork, and lyrics from Genius:

```bash
music-downloader "Song Title"
```

By default, files are saved in your Music directory, but you can specify a custom directory with the `--output_dir` option:

```bash
music-downloader "Song Title" --output_dir "/path/to/save/music"
```

### Downloading by YouTube URL

If you have a specific YouTube URL, you can still use it with the downloader. However, it may miss some metadata, so using the song title is recommended for a richer media experience.

```bash
music-downloader "https://www.youtube.com/watch?v=EXAMPLE_VIDEO_ID"
```

For YouTube playlists, simply provide the playlist URL:

```bash
music-downloader "https://www.youtube.com/playlist?list=EXAMPLE_PLAYLIST_ID"
```

In both cases, **Music Downloader** will download each video in the playlist and try to match metadata from Genius for each song.

### Example Commands

```bash
# Recommended method for best metadata
music-downloader "Let Me Down Slowly Alec Benjamin"

# Using a single YouTube video URL
music-downloader "https://www.youtube.com/watch?v=EXAMPLE_VIDEO_ID"

# Using a YouTube playlist URL
music-downloader "https://www.youtube.com/playlist?list=EXAMPLE_PLAYLIST_ID"
```

### Command-Line Options

- `input`: The YouTube URL, playlist URL, or song title you want to download.
- `--output_dir`: Custom directory to save the downloaded audio. Defaults to `~/Music`.

## Development

If you'd like to contribute or experiment with the code, fork and clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/music_downloader.git
cd music_downloader
pip install -r requirements.txt
```

### Running Locally

To run the downloader locally:

```bash
python -m music_downloader.downloader "Song Title"
```

## Contribution

We welcome contributions to improve **Music Downloader**! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes, and ensure all code is properly documented and tested.
4. Submit a pull request with a detailed explanation of your changes.

Please make sure your contributions align with the project’s code style and conventions. Feel free to open an issue if you'd like to discuss your contribution before starting.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading YouTube audio.
- Metadata and lyrics from [Genius](https://genius.com/).

## Support

For issues or feature requests, please open an issue on [GitHub](https://github.com/AQaddora/music_downloader/issues).