from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import User, RequestFriends, UserFriends, ProfilePost, LikesPost
from .forms import *


# Create your views here.
class RegistrationView(CreateView):
	template_name = 'users/registration.html'
	model = User
	form_class = RegistrationUser


	def get_success_url(self):
		return reverse('messanger:index')


	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return HttpResponseRedirect(reverse('messanger:index'))


class LoginUserView(LoginView):

	template_name = 'users/login.html'
	model = User
	form_class = LoginUser


	def get_success_url(self):
		return reverse('messanger:index')


def user_profile(request, pk):

	form = EditUserInfo(instance=request.user)
	form_create_post = CreatePostForm()

	if request.method == 'POST':
		if 'profile_change' in request.POST:
			form = EditUserInfo(data=request.POST, files=request.FILES, instance=request.user)
			if form.is_valid():			
				form.save()

		elif 'create_post' in request.POST:
			pp = ProfilePost(
				user=request.user,
				text=request.POST.get('text'),
				img=request.FILES.get('img')
			)
			pp.save()

	context = {'form': form, 'form_create_post': form_create_post}
	context['user_profile'] = User.objects.get(pk=pk)

	if pk != request.user.id:
		owner = request.user
		friend = User.objects.get(pk=pk)

		if len(RequestFriends.objects.filter(user_send_id=owner.id).filter(user_accept_id=friend.id).all())>=1:
			context['friend_status'] = 'request_sent'
		
		elif len(UserFriends.objects.filter(owner_id=owner.id).filter(friend_id=friend.id).all())>=1:
			context['friend_status'] = 'in_friendlist'

		else:
			context['friend_status'] = 'add_friend'

	if len(User.objects.get(pk=pk).profilepost_set.all())>=1:
		context['post_list'] = ProfilePost.objects.filter(user_id=pk).order_by('-pub_date').all()


	return render(request, 'users/profile.html', context=context)


def accept_friend(request, senter_id, accepter_id):

	request_friendlist = RequestFriends.objects.filter(
		user_send_id=senter_id
	).filter(
		user_accept_id=accepter_id
	).first()

	request_friendlist.accept = True

	owner = request_friendlist.user_send
	friend = request_friendlist.user_accept

	request_friendlist.delete()


	uf_for_user1 = UserFriends(owner = owner, friend = friend)
	uf_for_user2 = UserFriends(owner=friend, friend=owner)

	uf_for_user1.save()
	uf_for_user2.save()

	return HttpResponseRedirect(reverse('users:friend_list', kwargs={'pk':request.user.id}))


def reject_friend(request, senter_id, accepter_id):

	request_friendlist = RequestFriends.objects.filter(
		user_send_id=senter_id
	).filter(
		user_accept_id=accepter_id
	).delete()

	return HttpResponseRedirect(reverse('users:profile', kwargs={'pk':accepter_id}))


def create_request_friends(request, senter_id, accept_id):

	if request.user.id == senter_id:
		if len(RequestFriends.objects.filter(user_send_id=senter_id).filter(user_accept_id=accept_id))<1:
			request_to_friends = RequestFriends(
				user_send = request.user,
				user_accept = User.objects.get(pk=accept_id),
				accepted = False
			)
			request_to_friends.save()

	return HttpResponseRedirect(reverse('users:profile', kwargs={'pk':accept_id}))


def delete_friend(request, owner_id, friend_id):

	UserFriends.objects.filter(owner_id=owner_id).filter(friend_id=friend_id).delete()
	UserFriends.objects.filter(owner_id=friend_id).filter(friend_id=owner_id).delete()


	return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': friend_id}))


def check_friend_list(request, pk):

	context = {}

	if request.user.id == pk:

		if request.method == 'POST' and 'found_user' in request.POST:
			login_to_found = request.POST.get('found_user')
			try:
				context['found_user'] = User.objects.filter(username=login_to_found).first()
			except:
				context['found_user'] = 'Пользователь был не найден'

		return render(request, 'users/friend_list.html', context=context)

	return HttpResponseRedirect(reverse('messanger:index'))


def post_handler(request, pk, user_id):

	post = ProfilePost.objects.get(pk=pk)



	if request.method == 'GET':

		if request.GET.get('add_like'):

			if len(LikesPost.objects.filter(user_id=request.user.id).filter(post_id = post.id).all()) <= 1:
				lp = LikesPost(
					user = request.user,
					post = post
				)
				lp.save()

		elif request.GET.get('delete_like'):
			if len(LikesPost.objects.filter(user_id=request.user.id).filter(post_id = post.id).all()) >= 1:
				LikesPost.objects.filter(user_id=request.user.id).filter(post_id=post.id).first().delete()


		elif request.GET.get('delete_post'):
			if request.user.id == user_id:
				ProfilePost.objects.get(pk=pk).delete()


	return HttpResponseRedirect(reverse('users:profile', kwargs={'pk':post.user.id}))


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('users:login'))