
from django.urls import path, include


app_urls = [
    path('ckeditor/', include('ckeditor_uploader.urls'))
]
