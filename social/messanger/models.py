from django.db import models
from django.utils import timezone

from users.models import User

# Create your models here.
class Chat(models.Model):
	user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
	with_user = models.ForeignKey(User, related_name='chat_with', on_delete=models.CASCADE)


class Message(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	chat = models.ForeignKey(Chat, related_name='msg', on_delete=models.CASCADE)
	text = models.TextField()
	date = models.DateTimeField(default=timezone.now)