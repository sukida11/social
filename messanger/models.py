from django.db import models
from django.utils import timezone

from users.models import User

# Create your models here.

class Message(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	date = models.DateTimeField(default=timezone.now)


class Chat(models.Model):
	users = models.ManyToManyField(User)
	messages = models.ManyToManyField(Message)