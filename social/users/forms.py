from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from .models import User, ProfilePost

class RegistrationUser(UserCreationForm):

	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2 mr-sm-2', 'placeholder': 'Имя'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2 mr-sm-2', 'placeholder': 'Фамилия'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2 mr-sm-2', 'placeholder': 'Логин'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control mb-2 mr-sm-2', 'placeholder': 'Электронная почта'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-2 mr-sm-2', 'placeholder': 'Придумайте пароль'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-2 mr-sm-2', 'placeholder': 'Повторите пароль'}))

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginUser(AuthenticationForm):

	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2 mr-sm-2'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-2 mr-sm-2'}))

	class Meta:
		model = User
		fields = ['username', 'password']


class EditUserInfo(UserChangeForm):
	
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2 mr-sm-2'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2 mr-sm-2', 'placeholder': 'Фамилия'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2 mr-sm-2', 'readonly': True}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control mb-2 mr-sm-2', 'readonly': True}))
	img = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'style': 'width: 350px;'}), required=False)


	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'img']
		

class CreatePostForm(forms.Form):


	user = forms.CharField(widget=forms.HiddenInput(attrs={'name': 'user_id', 'value': '{{user.id}}'}))
	text = forms.CharField(widget=forms.Textarea(attrs={
			'class': 'form-control',
			'cols': '46',
			'rows': '16',
			'placeholder': 'Максимальное кол-во символов 800. Для переноса строки используйте ENTER',
			'maxlength': '800',
			'style': 'resize: none;'
		}))
	img = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

	class Meta:
		model = ProfilePost
		fields = ['text', 'img']