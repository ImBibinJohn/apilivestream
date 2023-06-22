from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    video = models.FileField(upload_to='videos/')

class StreamData(models.Model):
    # Define fields to store the relevant data from the RTMP stream
    # Adjust the fields based on the actual data you want to save
    timestamp = models.DateTimeField(auto_now_add=True)
    video_url = models.CharField(max_length=200)
    audio_url = models.CharField(max_length=200)

    def __str__(self):
        return f"StreamData ID: {self.id}"
