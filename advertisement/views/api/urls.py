# devices/urls.py

from django.urls import path
from .views import DeviceUploadView,MediaFetch,BranchFetch

urlpatterns = [
    path('upload_device/', DeviceUploadView.as_view(), name='upload_device'),
    path('<str:device_id>/get_media/', MediaFetch.as_view(), name='get_media'),
    path('branchList/', BranchFetch.as_view(), name= 'branch_List')
]
