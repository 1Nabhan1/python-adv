from django.db import models
from django.utils import timezone
# Create your models here.
class Device(models.Model):
    device_id = models.CharField(max_length=50,unique=True)
    branch_name = models.CharField(max_length=100,blank=True,null=True)
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

    media_url = models.URLField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, to_field='device_id', db_column='device_id')

    def __str__(self):
        return self.media_url