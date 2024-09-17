
# Discord YouTube Video Downloader and Splitter Bot

This Discord bot allows users to download YouTube videos and split them into multiple segments. The bot needs to be hosted locally to work properly and offers the following functionalities.

## Features
- **List video formats**: Use `!formats <YouTube URL>` to list available formats for a video.
- **Download video**: Use `!download <YouTube URL> <format_code> <optional_output_name>` to download a video in a specific format.
- **Split video**: Use `!split <video_file> <segment_duration> <optional_output_pattern>` to split the video into smaller parts.

## Requirements
- Python 3.8+
- `discord.py` library
- `yt-dlp` for downloading videos from YouTube
- `ffmpeg` for splitting videos

## Installation
1. Clone this repository or download the source code.
2. Install the required dependencies:
   ```bash
   pip install discord.py
   pip install yt-dlp
   ```
3. Ensure `ffmpeg` is installed on your system and accessible in your PATH.

## Usage
1. Run the bot using the following command:
   ```bash
   python bot.py
   ```
2. Use the commands in any Discord channel where the bot has permissions:
   - `!formats <YouTube URL>`: Lists all available video formats.
   - `!download <YouTube URL> <format_code>`: Downloads the YouTube video in the specified format.
   - `!split <video_file> <segment_duration>`: Splits the video into segments of the given duration.

## Permissions
Ensure the bot has the following permissions in your server:
- Manage Messages
- Send Messages
- Attach Files (if needed)

## Hosting Locally
This bot needs to be hosted locally. Make sure your environment has access to `yt-dlp` and `ffmpeg` tools for video downloading and splitting.

## License
This project is open-source. Feel free to modify and distribute it as needed.

### Example Commands
- `!formats https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- `!download https://www.youtube.com/watch?v=dQw4w9WgXcQ 22`
- `!split video_output.mp4 00:03:00`

