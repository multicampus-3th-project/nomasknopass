from django.urls import path

from . import views

app_name = 'kf99'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]