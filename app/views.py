from django.shortcuts import render,redirect
from app.models import *
from django.http import JsonResponse,HttpResponse
import subprocess
from django.conf import settings
import os
import signal

def index(request):
    return render(request,'index.html')

def save_form(request):
    if request.method == 'POST':
        if request.POST.get('name') == "" or request.FILES.get('image') is None or request.FILES.get('video') is None:
            return JsonResponse({'success': False, 'message': 'Fill All Fields'})
        else:
            name = request.POST.get('name')
            image = request.FILES.get('image')
            video = request.FILES.get('video')

            # Perform database operations here to save the form data
            save_db = Item.objects.create(name=name, image=image, video=video)

            # Return a JSON response
            return JsonResponse({'success': True, 'message': 'Form data saved successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid Request Type'})


def redirection(request):
    url = 'rtmp://localhost:1935/live/test'
    return JsonResponse({'success':True,'message': url})

def show_video(request):
    video = Item.objects.latest('id')
    video_url = "/media/" + str(video.video)  # Assuming 'url' is the attribute containing the video URL
    video_html = '<video id="videoElement" src="' + video_url + '" controls width="400" height="280"></video>'
    return HttpResponse(video_html)

FFMPEG_PROCESS = None

def extract_rtmp_data(request):
    global FFMPEG_PROCESS

    url = 'rtmp://localhost:1935/live/test'
    video_file_path = os.path.join(settings.MEDIA_ROOT, 'data', 'stream.m3u8')
    audio_file_path = 'audio_url_placeholder'  # Update this with the actual audio file path

    if FFMPEG_PROCESS is None:
        ffmpeg_command = [
            'ffmpeg', '-v', 'verbose', '-i', url,
            '-vf', 'scale=1920:1080', '-vcodec', 'libx264', '-r', '25', '-b:v', '1000000',
            '-crf', '31', '-acodec', 'aac', '-sc_threshold', '0', '-f', 'hls',
            '-hls_time', '5', '-segment_time', '5', '-hls_list_size', '5', 'stream.m3u8'
        ]

        try:
            FFMPEG_PROCESS = subprocess.Popen(ffmpeg_command, preexec_fn=os.setsid, shell=False)
        except subprocess.CalledProcessError as e:
            # Handle any errors that occur during the subprocess execution
            # You can log the error or raise an exception if desired
            print(f"Error occurred: {e}")
            return render(request, 'error_template.html')  # Render an error template if the subprocess fails

    # Save the data to the database
    stream_data = StreamData.objects.create(video_file=video_file_path, audio_file=audio_file_path)

    # Return the rendered template with the URL
    return render(request, 'stream_data.html', {'url': url})

def stop_rtmp_data(request):
    global FFMPEG_PROCESS

    if FFMPEG_PROCESS is not None:
        os.killpg(os.getpgid(FFMPEG_PROCESS.pid), signal.SIGTERM)
        FFMPEG_PROCESS = None

    return render(request, 'stream_stopped.html')




