import argparse
import os
import re
import shutil
import tempfile
import requests
import yt_dlp
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT, APIC

GENIUS_API_KEY = 'L0BY-i4ZVi0wQ53vlvm2zucqjHTuLbHv--YgjxJoN0spnEIhb5swTr_mWlQ6Ye-F'

def sanitize_filename(filename):
    """Sanitize filename to avoid issues with special characters."""
    return re.sub(r'[\\/:"*?<>|]+', "_", filename)

def is_youtube_url(input_string):
    """Check if the input string is a YouTube URL."""
    return "youtube.com" in input_string or "youtu.be" in input_string

def search_youtube(song_title):
    """Search for the song on YouTube and return the first video URL and metadata."""
    ydl_opts = {'quiet': True, 'format': 'bestaudio/best', 'noplaylist': True}
    search_url = f"ytsearch:{song_title}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(search_url, download=False)
        video_url = result['entries'][0]['webpage_url']
        music_metadata = result['entries'][0]
        return video_url, music_metadata

def fetch_genius_metadata(song_title, artist=None):
    """Fetch song metadata, including lyrics and album art, from Genius."""
    headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
    params = {"q": f"{song_title} {artist}" if artist else song_title}
    response = requests.get("https://api.genius.com/search", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['response']['hits']:
            song_data = data['response']['hits'][0]['result']
            title_with_featured = song_data.get('title_with_featured') or song_data.get('title')
            song_url = song_data['url']
            song_art_url = song_data['song_art_image_url']
            primary_artist = song_data['primary_artist']['name']
            release_date = song_data.get('release_date_for_display')
            lyrics = scrape_lyrics_from_url(song_url)
            return {
                "title": title_with_featured,
                "artist": primary_artist,
                "album": "Single",
                "release_date": release_date,
                "song_art_url": song_art_url,
                "lyrics": lyrics
            }
    print("No metadata found for this song on Genius.")
    return None

def scrape_lyrics_from_url(url):
    """Scrape lyrics directly from the Genius song page."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        lyrics_container = soup.find_all("div", attrs={"data-lyrics-container": "true"})
        if lyrics_container:
            return "\n".join([container.get_text(separator="\n") for container in lyrics_container])
    return None

def embed_metadata(file_path, metadata):
    """Embed metadata including title, artist, album, artwork, and lyrics into the MP3 file."""
    if metadata is None:
        print("No metadata to embed.")
        return
    
    audio = EasyID3(file_path)
    audio['title'] = metadata.get('title', 'Unknown Title')
    audio['artist'] = metadata.get('artist', 'Unknown Artist')
    audio['album'] = metadata.get('album', 'Unknown Album')
    audio.save()

    # Embed lyrics if available
    if metadata.get('lyrics'):
        audio = ID3(file_path)
        audio["USLT"] = USLT(encoding=3, lang='eng', desc='Lyrics', text=metadata['lyrics'])
        audio.save()
        print("Lyrics embedded in the MP3 file.")
    
    # Embed artwork if available
    if metadata.get('song_art_url'):
        try:
            art_response = requests.get(metadata['song_art_url'])
            art_response.raise_for_status()
            audio = ID3(file_path)
            audio["APIC"] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc='Cover',
                data=art_response.content
            )
            audio.save()
            print("Artwork embedded in the MP3 file.")
        except Exception as e:
            print(f"Failed to embed artwork: {e}")
    else:
        print("No artwork found to embed.")

def download_audio(video_url, output_dir, metadata):
    """Download audio from YouTube, convert it to MP3, embed metadata, then move file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Use sanitized title for both temp and final filenames
        title = sanitize_filename(metadata['title']) if metadata else "audio"
        ydl_opts = {
            'quiet': True, 
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, f"{title}.%(ext)s"),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }
            ],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f'Downloading {title}...')
            info = ydl.extract_info(video_url, download=True)
            downloaded_file = os.path.join(temp_dir, f"{title}.mp3")
            
            # Check if the downloaded file exists before embedding metadata
            if not os.path.exists(downloaded_file):
                print(f"Error: Downloaded file {downloaded_file} not found. Conversion may have failed.")
                return  # Exit the function if the file is missing
            
            # Embed metadata before moving to the output directory
            embed_metadata(downloaded_file, metadata)

            # Move to the output directory as the final step
            final_file = os.path.join(output_dir, f"{title}.mp3")
            shutil.move(downloaded_file, final_file)
            print(f"Downloaded and saved '{title}' to {output_dir}")

def clean_title(youtube_title):
    # Remove content within parentheses
    title = re.sub(r'\(.*?\)', '', youtube_title)
    # Remove common phrases
    common_phrases = ['Official Audio', 'Official Video', 'Official Music Video', 'prod.', 'Prod.']
    for phrase in common_phrases:
        title = title.replace(phrase, '')
    # Split the title on '|' and select the part with more non-space characters
    parts = title.split('|')
    if len(parts) == 1:
        title = parts[0]
    else:
        title = max(parts, key=lambda s: len(s.strip()))
    return title.strip()

def extract_artist_and_title(cleaned_title):
    # Split on '-' and '|'
    delimiters = ['-', '|']
    regex_pattern = '|'.join(map(re.escape, delimiters))
    parts = re.split(regex_pattern, cleaned_title)
    parts = [part.strip() for part in parts if part.strip()]

    if len(parts) >= 2:
        # Assuming the first part is the artist, the second is the title
        artist = parts[0]
        title = parts[1]
    else:
        artist = 'Unknown Artist'
        title = cleaned_title.strip()
    
    return artist, title


def process_info_dict(info, output_dir):
    if info.get('_type', 'video') == 'playlist':
        # It's a playlist
        print(f"Processing playlist: {info.get('title', 'Unknown Playlist')}")
        for entry in info['entries']:
            if entry is None:
                continue  # Entry could be None
            process_info_dict(entry, output_dir)
    elif info.get('_type', 'video') in ('url', 'url_transparent'):
        # Need to extract info from the URL provided in 'url' key
        with yt_dlp.YoutubeDL() as ydl:
            new_info = ydl.extract_info(info['url'], download=False)
            process_info_dict(new_info, output_dir)
    else:
        # It's a video
        youtube_title = info['title']
        cleaned_title = clean_title(youtube_title)
        artist, title = extract_artist_and_title(cleaned_title)

        # Attempt to fetch Genius metadata
        genius_metadata = fetch_genius_metadata(f"{title}")
        if genius_metadata:
            print("Genius metadata found.")
            metadata = genius_metadata
        else:
            print("Genius metadata not found, using YouTube metadata.")
            metadata = {
                "title": title,
                "artist": artist,
                "album": "Single"
            }
        video_url = info.get('webpage_url', info.get('url'))
        download_audio(video_url, output_dir, metadata)

def main():
    try:
        parser = argparse.ArgumentParser(description="Download music and fetch metadata from Genius.")

        DEFAULT_OUTPUT_DIR = os.path.join(
            os.path.expanduser("~"), "Music") if os.name == "nt" else "~/Music/Music/Media.localized/Automatically Add to Music.localized"

        parser.add_argument("input", help="YouTube URL, playlist URL, or song name to search and download")
        parser.add_argument("--output_dir", help="Directory to save the downloaded audio", default=DEFAULT_OUTPUT_DIR)

        args = parser.parse_args()

        output_dir = os.path.expanduser(args.output_dir)
        os.makedirs(output_dir, exist_ok=True)

        if is_youtube_url(args.input):
            print("Input recognized as a YouTube URL.")
            video_url = args.input
            ydl_opts = {'quiet': True, 'format': 'bestaudio/best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print('Extracting info...')
                info = ydl.extract_info(video_url, download=False)
                process_info_dict(info, output_dir)
        else:
            print("Input recognized as a song name.")
            # Attempt to fetch Genius metadata
            metadata = fetch_genius_metadata(args.input)

            # If Genius metadata is found, use it; otherwise, fall back to YouTube metadata
            if metadata:
                video_url, _ = search_youtube(metadata.get('title', args.input))
                print("Genius metadata found.")
            else:
                print("Song not found on Genius, falling back to YouTube metadata.")
                video_url, youtube_metadata = search_youtube(args.input)
                metadata = {
                    "title": youtube_metadata['title'],
                    "artist": youtube_metadata.get('artist', 'Unknown Artist'),
                    "album": "Single"
                }

            # Download audio using the available metadata (Genius or YouTube)
            download_audio(video_url, output_dir, metadata)
            print("All downloads and metadata processing completed.")
    except KeyboardInterrupt:
        print('Adiós!')

if __name__ == "__main__":
    main()
