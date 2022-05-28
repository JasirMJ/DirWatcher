from django.urls import include, path

from dirRecord.views import DirFilesAPI, DirRecordAPI

urlpatterns = [
    path('', DirRecordAPI.as_view()),
    path('files/', DirFilesAPI.as_view()),
    

]
