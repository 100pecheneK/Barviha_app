from django.urls import path
from . import views

app_name = 'yandex_xml'
urlpatterns = [
    path('yandex_feed/<str:slug>', views.xml_feed, name='xml_feed'),
]
