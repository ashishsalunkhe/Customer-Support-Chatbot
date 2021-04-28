from django.urls import path, include
from Tensorflow_Chatbot import views

urlpatterns = [
    path('', views.index),
    path('api', include("Tensorflow_Chatbot.Api.urls")),

]
