import typer
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

app = typer.Typer()

@app.command()
def download_video(
    url: str,
    writethumbnail: bool = typer.Option(True, "--writethumbnail", "-wt", help="Write thumbnail to disk as a separate file"),
    preferredquality: str = typer.Option("192", "--preferredquality", "-pq", help="Preferred audio quality ('192' or '256')"),
    preferredcodec: str = typer.Option("mp3", "--preferredcodec", "-pc", help="Preferred audio codec (m4a, mp3, mp4, webm)"),
):
    '''Youtube MP3 download'''
    ydl_opts = {
        'format': 'bestaudio/best',
        'writethumbnail': writethumbnail,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': preferredcodec,
            'preferredquality': preferredquality,
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }

    if writethumbnail:
        ydl_opts['postprocessors'].append({
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': False,
        })

    ydl_opts['postprocessors'].append({
        'key': 'FFmpegMetadata',
        'add_metadata': 'True',
    })

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except DownloadError as e:
        typer.echo(f"Download failed: {e}")
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app()
