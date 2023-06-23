from django.shortcuts import render,redirect
from app.models import *
from django.http import JsonResponse,HttpResponse
import requests
import random
import string
import ffmpeg
from .models import StreamData

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
    video_url = "/media/" + str(video.video) # Assuming 'url' is the attribute containing the video URL
    print('video_url : ',video_url)
    return HttpResponse('<video src="' + video_url + '" controls width="400" height="280"></video>')



def extract_rtmp_data(request):
    stream_url = 'rtmp://localhost:1935/live/test'
    print(stream_url)

    probe = ffmpeg.probe(stream_url)
    print(probe)

    video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
    audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']

    video_url = video_streams[0].get('url') if video_streams else None
    audio_url = audio_streams[0].get('url') if audio_streams else None

    # Save the extracted data to the database
    stream_data = StreamData.objects.create(
        video_url=video_url or '',
        audio_url=audio_url or ''
    )

    # Retrieve all saved stream data from the database
    all_stream_data = StreamData.objects.all()

    # Pass the retrieved data to the HTML template
    context = {'stream_data': all_stream_data}

    # Render the HTML template and return the response
    return render(request, 'stream_data.html', context)


