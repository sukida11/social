from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
	path('registration/', RegistrationView.as_view(), name='reg'),
	path('login/', LoginUserView.as_view(), name='login'),
	path('logout/', user_logout, name='user_logout'),
	path('profile/<int:pk>/', user_profile, name='profile'),
	path('add-friend/<int:senter_id>/<int:accepter_id>/', accept_friend, name='accept_friend'),
	path('reject-friend-request/<int:senter_id>/<int:accepter_id>/', reject_friend, name='reject_friend'),
	path('create-request-friends/<int:senter_id>/<int:accept_id>/', create_request_friends, name='create_request_friends'),
	path('delete-friend/<int:owner_id>/<int:friend_id>', delete_friend, name='delete_friend'),
	path('friend-list/<int:pk>/', check_friend_list, name='friend_list'),
	path('post-handler/<int:pk>/<int:user_id>/', post_handler, name='post_handler')
]