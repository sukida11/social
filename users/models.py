from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
class User(AbstractUser):
	img = models.ImageField(upload_to='profile_photo/', blank=True)


class RequestFriends(models.Model):
	user_send = models.ForeignKey(User, related_name='send', on_delete=models.CASCADE)
	user_accept = models.ForeignKey(User, related_name='accept', on_delete=models.CASCADE)
	accepted = models.BooleanField(default=False)



class UserFriends(models.Model):
	owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
	friend = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)


class ProfilePost(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.CharField(max_length=800)
	img = models.ImageField(upload_to='post_photo/', blank=True)
	pub_date = models.DateTimeField(default=timezone.now)


class LikesPost(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(ProfilePost, on_delete=models.CASCADE)


class Comment(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(ProfilePost, on_delete=models.CASCADE)
	text = models.TextField()
	date = models.DateTimeField(default=timezone.now)
