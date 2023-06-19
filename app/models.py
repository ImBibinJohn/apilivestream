from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    video = models.FileField(upload_to='videos/')
