from django.urls import path

from .views import upload_file

app_name = 'requestdataapp'

urlpatterns = [
    path('uploadfile/', upload_file, name='uploadfile'),
]
