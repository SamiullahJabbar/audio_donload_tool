# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.http import FileResponse
# import yt_dlp
# import os
# import tempfile
#
#
# # ==============================================================================
# # VIEW 1: Video aur Audio ki Information Nikalne ke liye
# # ==============================================================================
# class VideoInfoAPIView(APIView):
#     def post(self, request):
#         url = request.data.get('url')
#         if not url:
#             return Response({'error': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         ydl_opts = {'quiet': True}
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             try:
#                 info = ydl.extract_info(url, download=False)
#
#                 # --- VIDEO FORMATS (Direct Download Links) ---
#                 # Hum sirf woh formats nikalenge jin mein video aur audio pehle se mojood hain.
#                 # Isse user ke browser mein direct download hoga, server par load nahi aayega.
#                 video_formats = []
#                 processed_resolutions = set()
#
#                 # Formats ko behtar quality se kam quality ki taraf sort karein
#                 sorted_formats = sorted(info.get('formats', []), key=lambda f: f.get('height') or 0, reverse=True)
#
#                 for fmt in sorted_formats:
#                     # Check karein ke format mein video aur audio dono hain
#                     if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
#                         resolution = f"{fmt.get('height')}p"
#                         # Ek resolution ka sirf ek hi format (behtareen wala) show karein
#                         if resolution not in processed_resolutions:
#                             video_formats.append({
#                                 'resolution': resolution,
#                                 'ext': fmt.get('ext'),
#                                 'filesize': fmt.get('filesize') or fmt.get('filesize_approx'),
#                                 'download_url': fmt.get('url')  # YEH DIRECT DOWNLOAD LINK HAI
#                             })
#                             processed_resolutions.add(resolution)
#
#                 # --- AUDIO FORMAT (MP3 Conversion ke liye) ---
#                 # Hum sabse achi audio ka format_id frontend ko denge.
#                 # Frontend is id ko doosri API ko bhejega taake server usay MP3 bana sake.
#                 audio_formats = []
#                 best_audio = ydl.build_format_selector('bestaudio').get('format_id')
#                 if best_audio:
#                     audio_formats.append({
#                         'format': 'MP3',
#                         'quality': 'Best Available',
#                         # Is format_id ko MP3 conversion ke liye istemal karenge
#                         'format_id_for_conversion': best_audio
#                     })
#
#                 return Response({
#                     'title': info.get('title'),
#                     'thumbnail': info.get('thumbnail'),
#                     'video_formats': video_formats,  # Direct link wali videos
#                     'audio_formats': audio_formats,  # MP3 banane ke liye info
#                 })
#
#             except yt_dlp.utils.DownloadError as e:
#                 return Response({'error': 'Invalid URL or video not found.'}, status=status.HTTP_400_BAD_REQUEST)
#             except Exception as e:
#                 return Response({'error': f'An unexpected error occurred: {str(e)}'},
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
# # ==============================================================================
# # VIEW 2: Sirf Audio ko MP3 mein Convert aur Download karwane ke liye
# # ==============================================================================
# class GenerateDownloadLinkAPIView(APIView):
#     def post(self, request):
#         url = request.data.get('url')
#         format_id = request.data.get('format_id')  # Yeh 'format_id_for_conversion' hai
#
#         if not url or not format_id:
#             return Response({'error': 'URL and format_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Temporary file banayein jo istemal ke baad khud delete ho jayegi
#         # delete=False isliye taake hum iska path istemal kar sakein
#         temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
#         temp_filepath = temp_file.name
#         temp_file.close()  # File ko band karein taake yt-dlp isay likh sake
#
#         try:
#             ydl_opts = {
#                 # Sirf di hui audio format ko download karein
#                 'format': format_id,
#                 # Post-processor se audio extract karke MP3 banayein
#                 'postprocessors': [{
#                     'key': 'FFmpegExtractAudio',
#                     'preferredcodec': 'mp3',
#                     'preferredquality': '192',  # MP3 quality (e.g., 192kbps)
#                 }],
#                 # Output file ka naam (extension ke baghair)
#                 'outtmpl': temp_filepath.replace('.mp3', ''),
#                 'quiet': True,
#             }
#
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 # Video download karein (jo asal mein sirf audio download karke convert karega)
#                 ydl.download([url])
#
#             # File download ke liye tayyar hai, usay response mein bhejein
#             # FileResponse file ko user ko stream karta hai aur server par load kam rakhta hai
#             response = FileResponse(open(temp_filepath, 'rb'), as_attachment=True,
#                                     filename=f"{info.get('title', 'audio')}.mp3")
#             return response
#
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#         finally:
#             # Har haal mein temporary file ko delete karein (chahe error aaye ya na aaye)
#             # Isse server ki storage full nahi hogi
#             if os.path.exists(temp_filepath):
#                 os.remove(temp_filepath)


#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import yt_dlp
#
#
# class VideoInfoAPIView(APIView):
#     def post(self, request):
#         url = request.data.get('url')
#         if not url:
#             return Response({'error': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         ydl_opts = {
#             'quiet': True,
#             'no_warnings': True,
#             'format': 'bestvideo+bestaudio/best',  # Prefer combined formats
#         }
#
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             try:
#                 info = ydl.extract_info(url, download=False)
#                 formats = info.get('formats', [])
#
#                 available_formats = []
#                 audio_formats = []
#
#                 # First: Find all audio-only formats
#                 audio_formats = [
#                     fmt for fmt in formats
#                     if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none'
#                 ]
#
#                 # Second: Process all video formats
#                 for fmt in formats:
#                     if fmt.get('vcodec') == 'none':
#                         continue  # Skip audio-only
#
#                     resolution = fmt.get('height', 0)
#                     ext = fmt.get('ext', 'mp4')
#                     fps = fmt.get('fps', 30)
#
#                     # CASE 1: Combined video+audio format
#                     if fmt.get('acodec') != 'none':
#                         available_formats.append({
#                             'type': 'ready',
#                             'format_id': fmt['format_id'],
#                             'ext': ext,
#                             'resolution': f"{resolution}p",
#                             'quality': f"{resolution}p (auto)",
#                             'filesize': fmt.get('filesize', 0),
#                             'fps': fps,
#                             'note': 'Direct download with audio'
#                         })
#
#                     # CASE 2: Video-only (needs audio pairing)
#                     else:
#                         # Find best matching audio (same container format preferred)
#                         best_audio = next((
#                             audio for audio in audio_formats
#                             if audio.get('ext') == ext
#                         ), audio_formats[0] if audio_formats else None)
#
#                         if best_audio:
#                             available_formats.append({
#                                 'type': 'merge',
#                                 'video_id': fmt['format_id'],
#                                 'audio_id': best_audio['format_id'],
#                                 'ext': ext,
#                                 'resolution': f"{resolution}p",
#                                 'quality': f"{resolution}p (merge required)",
#                                 'video_filesize': fmt.get('filesize', 0),
#                                 'audio_filesize': best_audio.get('filesize', 0),
#                                 'fps': fps,
#                                 'note': 'Will merge video+audio during download'
#                             })
#
#                 # Sort by resolution (highest first)
#                 available_formats.sort(
#                     key=lambda x: int(x['resolution'].replace('p', '')),
#                     reverse=True
#                 )
#
#                 return Response({
#                     'title': info.get('title'),
#                     'thumbnail': info.get('thumbnail'),
#                     'duration': info.get('duration'),
#                     'formats': available_formats,
#                 })
#
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
# class GenerateDownloadLinkAPIView(APIView):
#     def post(self, request):
#         url = request.data.get('url')
#         format_id = request.data.get('format_id')  # For ready formats
#         video_id = request.data.get('video_id')    # For merge formats
#         audio_id = request.data.get('audio_id')    # For merge formats
#
#         if not url:
#             return Response({'error': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         ydl_opts = {
#             'quiet': True,
#             'no_warnings': True,
#             'format': f'{format_id}' if format_id else f'{video_id}+{audio_id}',
#             'merge_output_format': 'mp4',
#         }
#
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             try:
#                 info = ydl.extract_info(url, download=False)
#                 return Response({
#                     'download_url': info['url'],
#                     'title': info.get('title'),
#                     'ext': 'mp4',
#                 })
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#
#

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from yt_dlp import YoutubeDL
# from .serializers import VideoURLSerializer
# import os
# import shutil
# import subprocess
# from django.conf import settings


# class GetVideoInfoView(APIView):
#     def post(self, request):
#         serializer = VideoURLSerializer(data=request.data)
#         if serializer.is_valid():
#             url = serializer.validated_data['url']
#             temp_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
#             os.makedirs(temp_dir, exist_ok=True)

#             # Base yt-dlp options
#             ydl_opts = {
#                 'noplaylist': True,
#                 'quiet': True,
#                 'outtmpl': os.path.join(temp_dir, '%(title)s_%(height)s.%(ext)s'),
#                 'format': 'bestvideo[height>=240][height<=2160]+bestaudio/best[acodec!=none]/best',
#                 'merge_output_format': 'mp4',
#             }

#             # Check if ffmpeg is available and add post-processor
#             def check_ffmpeg():
#                 try:
#                     result = subprocess.run(['ffmpeg', '-version'],
#                                             stdout=subprocess.PIPE,
#                                             stderr=subprocess.PIPE,
#                                             check=True)
#                     return True
#                 except (subprocess.CalledProcessError, FileNotFoundError, OSError):
#                     return False

#             if check_ffmpeg():
#                 ydl_opts['postprocessors'] = [{
#                     'key': 'FFmpegVideoConvertor',
#                     'preferedformat': 'mp4',
#                 }]
#             else:
#                 # If no ffmpeg, use format that doesn't require merging
#                 ydl_opts['format'] = 'best[ext=mp4][height>=240][height<=2160]/best[height>=240][height<=2160]'

#             try:
#                 with YoutubeDL(ydl_opts) as ydl:
#                     # First extract info without downloading
#                     info = ydl.extract_info(url, download=False)

#                     # Get available formats for display
#                     available_formats = []
#                     added_resolutions = set()

#                     for f in info.get('formats', []):
#                         height = f.get('height')
#                         if height and 240 <= height <= 2160:
#                             resolution = f'{height}p'
#                             if resolution not in added_resolutions:
#                                 available_formats.append({
#                                     'format_id': f['format_id'],
#                                     'ext': f.get('ext', 'mp4'),
#                                     'resolution': resolution,
#                                     'filesize': f.get('filesize') or f.get('filesize_approx'),
#                                     'has_audio': f.get('acodec') != 'none',
#                                     'has_video': f.get('vcodec') != 'none'
#                                 })
#                                 added_resolutions.add(resolution)

#                     # Sort by resolution (highest first)
#                     available_formats.sort(key=lambda x: int(x['resolution'].replace('p', '')), reverse=True)

#                     # Now download the best format
#                     downloaded_info = ydl.extract_info(url, download=True)

#                     # Find the downloaded file
#                     downloaded_file = None
#                     for root, dirs, files in os.walk(temp_dir):
#                         for file in files:
#                             if file.endswith(('.mp4', '.mkv', '.webm')):
#                                 downloaded_file = os.path.join(root, file)
#                                 break
#                         if downloaded_file:
#                             break

#                     # Prepare response
#                     response_data = {
#                         'title': info.get('title'),
#                         'thumbnail': info.get('thumbnail'),
#                         'duration': info.get('duration'),
#                         'view_count': info.get('view_count'),
#                         'uploader': info.get('uploader'),
#                         'formats': available_formats
#                     }

#                     # If we have a downloaded file, add it to response
#                     if downloaded_file and os.path.exists(downloaded_file):
#                         filename = os.path.basename(downloaded_file)
#                         response_data['downloaded_file'] = {
#                             'path': downloaded_file,
#                             'size': os.path.getsize(downloaded_file),
#                             'url': f'{settings.MEDIA_URL}downloads/{filename}'
#                         }

#                     return Response(response_data)

#             except Exception as e:
#                 # Clean up on error
#                 if os.path.exists(temp_dir):
#                     shutil.rmtree(temp_dir, ignore_errors=True)
#                 return Response({'error': str(e)}, status=400)

#             # Don't clean up temp_dir here - let it be cleaned up after file is served
#             # You might want to implement a cleanup mechanism elsewhere

#         return Response(serializer.errors, status=400)




# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import FormatSerializer
# import uuid
# import os
# import subprocess

# class GetDownloadLinkView(APIView):
#     def post(self, request):
#         serializer = FormatSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response({
#                 'download_url': serializer.validated_data['url']
#             })
#         return Response(serializer.errors, status=400)







# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from pytube import YouTube
# import os
# import uuid
# import tempfile
# import io
# from moviepy.editor import AudioFileClip
# from django.http import StreamingHttpResponse
# from wsgiref.util import FileWrapper

# class YouTubeToMP3DownloadView(APIView):
#     def post(self, request):
#         url = request.data.get("url")
#         if not url:
#             return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             yt = YouTube(url)
#             stream = yt.streams.filter(only_audio=True).first()

#             # Create temp file for mp4
#             with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_mp4:
#                 stream.download(filename=temp_mp4.name)
#                 temp_mp4_path = temp_mp4.name

#             # Convert to MP3 in memory
#             mp3_buffer = io.BytesIO()
#             audioclip = AudioFileClip(temp_mp4_path)
#             audioclip.write_audiofile(mp3_buffer, codec='mp3')
#             audioclip.close()

#             # Clean temp file
#             os.remove(temp_mp4_path)

#             # Prepare response
#             mp3_buffer.seek(0)
#             response = StreamingHttpResponse(
#                 FileWrapper(mp3_buffer),
#                 content_type='audio/mpeg'
#             )
#             response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp3"'
#             return response

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import YouTubeURLSerializer
# from django.http import FileResponse
# import yt_dlp
# import tempfile
# import os

# # 🎬 API 1: VIDEO INFO
# class YouTubeInfoAPIView(APIView):
#     def post(self, request):
#         serializer = YouTubeURLSerializer(data=request.data)
#         if serializer.is_valid():
#             url = serializer.validated_data['url']
#             try:
#                 ydl_opts = {
#                     'quiet': True,
#                     'skip_download': True,
#                     'noplaylist': True
#                 }
#                 with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                     info = ydl.extract_info(url, download=False)
#                     return Response({
#                         'title': info.get('title'),
#                         'thumbnail': info.get('thumbnail'),
#                         'duration': info.get('duration'),
#                         'channel': info.get('uploader'),
#                         'video_id': info.get('id'),
#                         'webpage_url': info.get('webpage_url')
#                     })
#             except Exception as e:
#                 return Response({'error': str(e)}, status=500)
#         return Response(serializer.errors, status=400)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import YouTubeURLSerializer
# from django.http import FileResponse
# import yt_dlp
# import tempfile
# import os
# import re

# class StreamMP3APIView(APIView):
#     def post(self, request):
#         serializer = YouTubeURLSerializer(data=request.data)
#         if serializer.is_valid():
#             url = serializer.validated_data['url']

#             try:
#                 with tempfile.TemporaryDirectory() as temp_dir:
#                     def sanitize_filename(title):
#                         return re.sub(r'[\\/*?:"<>|]', "_", title)

#                     ydl_opts = {
#                         'outtmpl': os.path.join(temp_dir, '%(title).40s.%(ext)s'),
#                         'format': 'bestaudio/best',
#                         'ffmpeg_location': 'ffmpeg',  # ✔ FFmpeg path
#                         'quiet': True,
#                         'noplaylist': True,
#                         'postprocessors': [{
#                             'key': 'FFmpegExtractAudio',
#                             'preferredcodec': 'mp3',
#                             'preferredquality': '192',
#                         }],
#                     }

#                     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                         info = ydl.extract_info(url, download=True)
#                         raw_title = info.get('title', 'audio')
#                         safe_title = sanitize_filename(raw_title)
#                         mp3_file_path = os.path.join(temp_dir, f"{safe_title}.mp3")

#                     # ✅ Check if MP3 file was created
#                     if os.path.exists(mp3_file_path):
#                         response = FileResponse(open(mp3_file_path, 'rb'), content_type='audio/mpeg')
#                         response['Content-Disposition'] = f'attachment; filename="{safe_title}.mp3"'
#                         return response
#                     else:
#                         return Response(
#                             {'error': 'MP3 file not found (conversion may have failed)'}, status=500
#                         )

#             except Exception as e:
#                 return Response({'error': str(e)}, status=500)

#         return Response(serializer.errors, status=400)







import os
import uuid
import threading
import time
from urllib.parse import urlparse, parse_qs
from django.conf import settings
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from yt_dlp import YoutubeDL

TEMP_DIR = os.path.join(settings.MEDIA_ROOT, 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

# Track last saved file
last_saved_file = {'path': None}

def delete_file(path):
    if path and os.path.exists(path):
        os.remove(path)

class GetVideoInfoView(APIView):
    """
    POST /api/get-video-info/
    Body: { "url": "<YouTube URL>" }
    Response: { "title": "Video Title", "thumbnail": "thumbnail_url" }
    """
    def post(self, request):
        youtube_url = request.data.get('url')
        if not youtube_url:
            return Response({'error': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Clean URL to single video
            parsed = urlparse(youtube_url)
            qs = parse_qs(parsed.query)
            video_id = qs.get('v', [None])[0]
            if video_id:
                final_url = f'https://www.youtube.com/watch?v={video_id}'
            else:
                final_url = youtube_url

            ydl_opts = {'noplaylist': True}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(final_url, download=False)
                title = info.get('title', 'YouTube Audio')
                thumbnail = info.get('thumbnail')

            return Response({'title': title, 'thumbnail': thumbnail})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadAudioView(APIView):
    """
    POST /api/download-audio/
    Body: { "url": "<YouTube URL>", "title": "<Video Title>" }
    Response: direct file download
    """
    def post(self, request):
        youtube_url = request.data.get('url')
        title = request.data.get('title', 'youtube_audio')
        if not youtube_url:
            return Response({'error': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Clean URL to single video
            parsed = urlparse(youtube_url)
            qs = parse_qs(parsed.query)
            video_id = qs.get('v', [None])[0]
            if video_id:
                final_url = f'https://www.youtube.com/watch?v={video_id}'
            else:
                final_url = youtube_url

            # Safe filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
            unique_id = str(uuid.uuid4())[:8]
            filename_base = f"{safe_title}_{unique_id}"
            output_path = os.path.join(TEMP_DIR, filename_base)

            # Delete previous file if any
            delete_file(last_saved_file.get('path'))

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_path,  # without extension; yt_dlp will add .mp3
                'noplaylist': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([final_url])

            # Final mp3 file path
            final_filename = f"{filename_base}.mp3"
            file_path = os.path.join(TEMP_DIR, final_filename)

            # Confirm file exists
            if not os.path.exists(file_path):
                return Response({'error': f"File not found: {final_filename}"}, status=500)

            # Update last saved file
            last_saved_file['path'] = file_path

            # Auto delete after 10 minutes
            threading.Thread(target=lambda: (time.sleep(600), delete_file(file_path)), daemon=True).start()

            # Serve as attachment
            file_handle = open(file_path, 'rb')
            response = FileResponse(file_handle, content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{final_filename}"'
            return response

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
