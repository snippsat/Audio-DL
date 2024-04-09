import typer
from yt_dlp import YoutubeDL

app = typer.Typer()

@app.command()
def download_video(
    url: str,
    writethumbnail: bool = typer.Option(True, "--writethumbnail", "-wt", help="Write thumbnail to disk"),
    preferredquality: str = typer.Option("192", "--preferredquality", "-pq", help="Preferred audio quality(eg 256 or 320)"),
):
    '''Youtube MP3 download'''
    ydl_opts = {
        'format': 'bestaudio/best',
        'writethumbnail': writethumbnail,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
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

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    app()
