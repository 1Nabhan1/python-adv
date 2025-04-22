from django.db import models
from django.utils import timezone
# Create your models here.

class Branch(models.Model):
    branchName=models.CharField(max_length=100)
    
class Device(models.Model):
    device_id = models.CharField(max_length=50,unique=True)
    branch_name = models.CharField(max_length=100,blank=True,null=True)
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True)
    device_name = models.CharField(max_length=100, unique=True,blank=True,null=True)
    orientation = models.CharField(max_length=50)
    resolution = models.CharField(max_length=50)
    status = models.BooleanField(default=True)  # True = Active, False = Blocked

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.device_name


class Media(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    ANIMATION_TYPE_CHOICES = (
        ('fade in','Fade In'),
        ('zoom','Zoom'),
        ('rotate','Rotate'),
        ('slide','Slide')
    )
    animation_type = models.CharField(max_length=10,choices=ANIMATION_TYPE_CHOICES,null=True)
    media_file = models.FileField(upload_to='device_media/', null=True, blank=True)  # For both images and videos
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, to_field='device_id', db_column='device_id')
    duration = models.IntegerField(max_length=10, null=True)
    def __str__(self):
        return self.media_file.name  # This will return the filename of the media file

    def get_media_url(self):
        # If the file exists, return the full URL to the media
        return self.media_file.url if self.media_file else None
