from django.urls import path

from inbox import views

urlpatterns = [
    path("messages/", views.messages, name="messages"),
]
