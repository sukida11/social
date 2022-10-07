from django.urls import path

from .views import *

app_name = 'messanger'

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('chat/', chat_list, name='chats'),
	path('chat-view/<int:user>/<int:with_user>', chat_view, name='chat'),
	path('delete-message/', delete_msg, name='delete_msg')
]