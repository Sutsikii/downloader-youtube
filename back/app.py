from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json['url']
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    video_info = ydl.extract_info(url, download=False)
    video_title = video_info.get('title', 'video')
    video_ext = video_info.get('ext', 'mp4')
    video_filename = f"{video_title}.{video_ext}"
    video_path = os.path.join('downloads', video_filename)
    response = send_file(video_path, as_attachment=True)
    # supprimer le fichier après avoir envoyé la réponse
    os.remove(video_path)
    return response
if __name__ == '__main__':
    app.run(debug=True)