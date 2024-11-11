import yt_dlp
from flask import Flask, request

app = Flask(__name__)


@app.route("/download/song/", methods=["POST"])
def download_video():
    url = request.form.get("url")
    preference = request.form.get("preference")

    if not url:
        return {"message": "URL no proporcionada"}, 400

    # Configuración de opciones para yt-dlp
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": preference,
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return {"message": "Video descargado con éxito!"}, 200


if __name__ == "__main__":
    app.run(debug=True)
