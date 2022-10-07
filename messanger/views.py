from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from users.models import User
from .models import Chat, Message

# Create your views here.
class IndexView(TemplateView):
	template_name = 'messanger/index.html'


def chat_list(request):

	context = {}

	if request.method == 'GET':
		if 'add_new_chat' in request.GET:
				with_user_id = request.GET.get('with_user')
				with_user = User.objects.get(pk=with_user_id)

				if len(Chat.objects.filter(users__id=request.user.id).filter(users__id=with_user_id).all()) >= 1:
					context['error'] = 'Диалог с данным пользователем уже есть.'
				else:

					c = Chat()
					c.save()
					c.users.add(request.user, with_user)
					c.save()

					return HttpResponseRedirect(reverse('messanger:chats'))

		elif 'user' in request.GET and 'with_user' in request.GET:
			user = request.GET.get('user')
			with_user = request.GET.get('with_user')

			if int(user) == request.user.id:
				Chat.objects.filter(users__id=user).filter(users__id=with_user).delete()

			return HttpResponseRedirect(reverse('messanger:chats'))


	if len(Chat.objects.filter(users__id=request.user.id).all()) >= 1:
		context['chats'] = Chat.objects.filter(users__id=request.user.id).all()
		context['chats_with_id'] = []

		for chat in context['chats']:
			
			for user in chat.users.all():
				if user.username == request.user.username:
					continue
				else:
					context['chats_with_id'].append(user.id)

	else:
		context['chats'] = ''


	return render(request, 'messanger/chat_list.html', context=context)


def chat_view(request, user, with_user):
	context = {}
	context['chat'] = Chat.objects.filter(users__id=user).filter(users__id=with_user).first()
	context['with_user_dialog'] = User.objects.get(pk=with_user)

	if request.method == 'POST':
		if 'msg_text' in request.POST:
			c=Chat.objects.filter(users__id=user).filter(users__id=with_user).first()
			
			msg = Message(
				user=request.user,
				text=request.POST.get('msg_text')
			)
			msg.save()

			c.messages.add(msg)
			c.save()
			

	return render(request, 'messanger/chat.html', context=context)


def delete_msg(request):

	if request.method == 'GET':

		user_id = request.GET.get('user_id')
		with_user_id = request.GET.get('with_user_id')
		message_id = request.GET.get('message_id')

		if request.user.id == int(user_id):
			mc = Chat.objects.filter(messages__pk=message_id).first()
			m = mc.messages.get(pk=message_id).delete()


	return HttpResponseRedirect(reverse('messanger:chat', 
		kwargs={'user': user_id, 
				'with_user': with_user_id
				}
	))