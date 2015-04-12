from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

from django.forms import ModelForm
from django import forms

from src.models.userprofile import UserProfile

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm()
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect('/login/')
        else:
            return HttpResponse('FORM ERROR')
    else:
        user_form = UserForm()
        return render(request, 'signup.html', {'user_form': user_form})

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('login.html', {}, context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')