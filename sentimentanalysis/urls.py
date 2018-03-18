from django.urls import path
from . import views

app_name = "sentimentanalysis"

urlpatterns = [
    path("", views.index, name="index"),
    path("result/", views.result, name='result'),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("feedback/", views.feedback, name="feedback")
]
