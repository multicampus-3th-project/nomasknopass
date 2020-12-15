from django.urls import path

from . import views

app_name = 'kf99'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('gateprediction/', views.predict_mask_gate),
    path('cctvprediction/', views.predict_mask_cctv),
    path('visit/', views.insert_ispass),
    path('emergency/', views.notificate_emergency),

]