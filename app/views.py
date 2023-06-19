from django.shortcuts import render,redirect
from app.models import *
from django.http import JsonResponse

def index(request):
    return render(request,'index.html')

def save_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        # Perform database operations here to save the form data
        save_db = Item.objects.create(name=name, image=image, video=video)

        # Return a JSON response
        return JsonResponse({'message': 'Form data saved successfully.'})


