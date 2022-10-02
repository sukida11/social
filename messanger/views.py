from django.shortcuts import render
from django.views.generic import TemplateView

from users.models import User

# Create your views here.
class IndexView(TemplateView):
	template_name = 'messanger/index.html'
