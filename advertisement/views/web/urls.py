from django.urls import path
from .import views

urlpatterns = [
    path('devices/', views.device_list_view, name='device_list'),
    path('devices/update/<int:device_id>/', views.update_device, name='update_device'),
    path('device/edit_media_list/<int:device_id>/', views.edit_media_list, name='edit_media_list'),  # New URL for editing media
    path('device/upload_media/<int:device_id>/', views.upload_media, name='upload_media'),  # New URL for uploading media
    path('media/<int:media_id>/edit/', views.edit_media, name='edit_media'),
    path('devices/branch/add/', views.add_branch, name='add_branch'),
    path('devices/branch_list/', views.branch_list, name = 'branch_list'),
    path('devices/branch/update/<int:branch_id>/', views.update_branch, name='update_branch'),
]


   