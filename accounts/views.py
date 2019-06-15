from django.contrib.auth import authenticate,login,logout,get_user_model
from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404,HttpResponse
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView
from django import forms
from .forms import LoginForm,RegisterForm

User = get_user_model()

def login_view(request):
	next_ = request.GET.get('next',None)
	next_post = request.POST.get('next',None)
	redirect_path = next_ or next_post or None
	form = LoginForm(request.POST or None)
	if request.POST and form.is_valid():
		user = form.login(request)
		if user:
			login(request,user)
			if is_safe_url(redirect_path,request.get_host()): #proceeding to checkout
				return redirect(redirect_path)
			else:
				return redirect('home')
	return render(request,'accounts/login.html',{'form':form})

class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'accounts/register.html'
	success_url = '../login/'

def logout_view(request):
	print(request.user,'logged out')
	logout(request)
	return redirect('home')
	# modify it to stay the page,not redirect to login always.
	#a user may logout from checkout page