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
				with_user = request.GET.get('with_user')

				if len(Chat.objects.filter(user_id=request.user.id).filter(with_user_id=with_user).all()) >= 1:
					context['error'] = 'Диалог с данным пользователем уже есть.'
				else:
					c = Chat(
						user = request.user,
						with_user = User.objects.get(pk=with_user)
					)
					c2 = Chat(
						user=User.objects.get(pk=with_user),
						with_user=request.user
					)
					c.save()
					c2.save()
					return HttpResponseRedirect(reverse('messanger:chats'))

		elif 'user' in request.GET and 'with_user' in request.GET:
			user = request.GET.get('user')
			with_user = request.GET.get('with_user')

			Chat.objects.filter(user_id=user).filter(with_user_id=with_user).first().delete()
			Chat.objects.filter(user_id=with_user).filter(with_user_id=user).first().delete()

			return HttpResponseRedirect(reverse('messanger:chats'))


	if len(Chat.objects.filter(user_id=request.user.id).all()) >= 1:
		context['chats'] = Chat.objects.filter(user_id=request.user.id).all()
		context['chats_with_id'] = []

		for chat in context['chats']:
			context['chats_with_id'].append(chat.with_user.id)

		print(context['chats_with_id'])

	else:
		context['chats'] = []

	return render(request, 'messanger/chat_list.html', context=context)


def chat_view(request, user, with_user):
	context = {}
	context['chat'] = Chat.objects.filter(user_id=user).filter(with_user_id=with_user).first()
	context['with_user_dialog'] = User.objects.get(pk=with_user)

	if request.method == 'POST':
		if 'msg_text' in request.POST:
			msg1 = Message(
				user=request.user,
				chat=context['chat'],
				text=request.POST.get('msg_text')
			)
			msg1.save()

			msg2 = Message(
				user=request.user,
				chat=Chat.objects.filter(user_id=with_user).filter(with_user_id=user).first(),
				text=request.POST.get('msg_text')
			)
			msg2.save()

	return render(request, 'messanger/chat.html', context=context)