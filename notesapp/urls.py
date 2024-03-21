from django.contrib import admin
from django.urls import path, include
from .views import (
    UserAPIView,
    UserLoginAPIView,
    NoteListCreateAPIView,
    NoteGetPutAPIView,
)

urlpatterns = [
    path("register/", UserAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
    path("notes/", NoteListCreateAPIView.as_view()),
    path("notes/<uuid:notes_id>", NoteGetPutAPIView.as_view()),
]
