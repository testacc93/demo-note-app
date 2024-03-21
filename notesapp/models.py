from django.db import models
from uuid import uuid4
import datetime


class User(models.Model):
    user_id = models.UUIDField(default=uuid4, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Note(models.Model):
    note_id = models.UUIDField(default=uuid4, unique=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
