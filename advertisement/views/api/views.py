from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Device
from ...serializers import DeviceSerializer
from django.http import JsonResponse
from ...models import Device, Media

# Create your views here.

class DeviceUploadView(APIView):
    def post(self, request):
        # Deserialize incoming data
        serializer = DeviceSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the device details into the database
            serializer.save()
            return Response({"message": "Device details uploaded successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MediaFetch(APIView):
    def get(self, request, device_id):
        try:
            # Fetch device by the given device_id
            device = Device.objects.get(device_id=device_id)
        
            # Check if the device is blocked
            if not device.status:  # Device is blocked
                return JsonResponse({"error": "Device is blocked."}, status=403)

            # If the device is active, get associated media
            media_list = Media.objects.filter(device=device)

            # Prepare media data to return in response
            media_data = [
                {"media_url": media.media_url, "media_type": media.media_type}
                for media in media_list
            ]

            return JsonResponse({"media": media_data}, status=200)

        except Device.DoesNotExist:
            return JsonResponse({"error": "Device not found."}, status=404)
        
        
        
        
            