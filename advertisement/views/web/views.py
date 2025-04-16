from django.shortcuts import render, redirect, get_object_or_404
from ...models import Device
from ...models import Device, Media
from django.conf import settings
import os

def device_list_view(request):
    devices = Device.objects.all()
    return render(request, 'device_list.html', {'devices': devices})


def update_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    if request.method == 'POST':
        device_name = request.POST.get('device_name')
        branch_name = request.POST.get('branch_name')
        status = request.POST.get('status') == '1'  # True if 'Active', False if 'Blocked'

        device.device_name = device_name
        device.branch_name = branch_name
        device.status = status  # Update the status

        device.save()  # Save the updated device object

        return redirect('device_list')  # Redirect to device list or another page

    return render(request, 'update_device.html', {'device': device})


def upload_media(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    if request.method == 'POST' and request.FILES.get('media_file'):
        # Handle media file upload for the device
        media_file = request.FILES['media_file']
        media_type = request.POST.get('media_type', 'image')  # or 'video', etc.
        
        # Save the file to the media directory
        media_dir = os.path.join(settings.MEDIA_ROOT, 'device_media')  # Or any sub-directory you prefer
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # Save the file to the correct path
        file_path = os.path.join(media_dir, media_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in media_file.chunks():
                destination.write(chunk)

        # Save the media record to the database
        media = Media(device=device, media_url=f'device_media/{media_file.name}', media_type=media_type)
        media.save()

        return redirect('device_list')  # Redirect to device list or wherever needed

    return render(request, 'update_media.html', {'device': device})

def edit_media_list(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    media_list = Media.objects.filter(device=device)
    return render(request, 'edit_media.html', {'device': device, 'media_list': media_list,'MEDIA_URL': settings.MEDIA_URL})


def edit_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)

    if request.method == 'POST':
        new_file = request.FILES.get('new_media_file')
        new_type = request.POST.get('media_type')  # <--- grab new type from form

        # Handle new file upload
        if new_file:
            # Delete old file if it exists
            old_file_path = os.path.join(settings.MEDIA_ROOT, str(media.media_url))
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

            # Save new file
            new_file_name = new_file.name
            new_file_path = os.path.join(settings.MEDIA_ROOT, 'device_media', new_file_name)

            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            with open(new_file_path, 'wb+') as destination:
                for chunk in new_file.chunks():
                    destination.write(chunk)

            # Update media URL in DB
            media.media_url = f'device_media/{new_file_name}'

        # Always update media type from the form
        if new_type in dict(Media.MEDIA_TYPE_CHOICES):
            media.media_type = new_type

        media.save()

    return redirect('edit_media_list', device_id=media.device.id)
