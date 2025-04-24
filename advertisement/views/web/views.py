from django.shortcuts import render, redirect, get_object_or_404
from ...models import Device
from ...models import Device, Media, Branch
from django.conf import settings
import os
from django.http import HttpResponse

def device_list_view(request):
    devices = Device.objects.all()
    return render(request, 'device_list.html', {'devices': devices})

def branch_list(request):
    branches = Branch.objects.all()
    return render(request, 'branch_list.html', {'branches': branches})

def add_branch(request):
    if request.method == 'POST':
        branch_name = request.POST.get('branchName')
        if branch_name:
            Branch.objects.create(branchName=branch_name)
            return redirect('branch_list')
    return render(request, 'add_branch.html')

def update_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)

    if request.method == 'POST':
        new_name = request.POST.get('branchName')
        if new_name:
            branch.branchName = new_name
            branch.save()
            return redirect('branch_list')  # or wherever you want to redirect
        else:
            return HttpResponse("Branch name cannot be empty.")

    return render(request, 'update_branch.html', {'branch': branch})


def update_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    if request.method == 'POST':
        device_name = request.POST.get('device_name')
        branch_name = device.branch.branchName if device.branch else "No Branch"
        status = request.POST.get('status') == '1'  # True if 'Active', False if 'Blocked'

        device.device_name = device_name
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
        animation_type = request.POST.get('animation_type','fede in')
        duration = request.POST.get('duration',0)
        isAudio = request.POST.get('isAudio',1)
        # Create a Media instance and save it to the database
        media = Media(device=device, media_file=media_file, media_type=media_type, animation_type = animation_type, duration = duration, isAudio = isAudio)
        media.save()  # Django will automatically handle the file storage

        return redirect('device_list')  # Redirect to device list or wherever needed

    return render(request, 'update_media.html', {'device': device})

def edit_media_list(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    media_list = Media.objects.filter(device=device)
    
    # Pass media_list and MEDIA_URL to the template
    return render(request, 'edit_media.html', {
        'device': device, 
        'media_list': media_list,
    })

def edit_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)

    if request.method == 'POST':
        new_file = request.FILES.get('new_media_file')
        new_type = request.POST.get('media_type')  # <--- grab new type from form
        new_animation = request.POST.get('animation_type')
        new_duration = request.POST.get('duration')
        new_audio_opt = request.POST.get('isAudio')
        # Handle new file upload
        if new_file:
            # Delete old file if it exists
            old_file_path = os.path.join(settings.MEDIA_ROOT, str(media.media_file.name))  # Use media_file.name
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

            # Save new file
            new_file_name = new_file.name
            new_file_path = os.path.join(settings.MEDIA_ROOT, 'device_media', new_file_name)

            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            with open(new_file_path, 'wb+') as destination:
                for chunk in new_file.chunks():
                    destination.write(chunk)

            # Update media_file in DB (media_url was replaced by media_file)
            media.media_file.name = f'device_media/{new_file_name}'

        # Always update media type from the form
        if new_type in dict(Media.MEDIA_TYPE_CHOICES):
            media.media_type = new_type
        if new_animation in dict(Media.ANIMATION_TYPE_CHOICES):
            media.animation_type = new_animation
        if new_duration :
            media.duration = new_duration
        if new_audio_opt:
            media.isAudio = new_audio_opt
        media.save()

    return redirect('edit_media_list', device_id=media.device.id)
