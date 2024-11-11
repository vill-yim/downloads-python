import yt_dlp
from flask import Flask, request, send_file
import os

app = Flask(__name__)


@app.route("/download/", methods=["POST"])
def download_video():
    url = request.form.get("url")
    preference = request.form.get("preference")

    if not url:
        return {"message": "URL no proporcionada"}, 400

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "/tmp/%(title)s.%(ext)s",  # Cambio principal: usar /tmp/
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": preference,
                "preferredquality": "192",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return {"message": "Video descargado con éxito!"}, 200
    except Exception as e:
        return {"message": f"Error: {str(e)}"}, 500


if __name__ == "__main__":
    app.run()
