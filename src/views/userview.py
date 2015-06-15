from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

from django import forms

from src.models.userprofile import UserProfile
from src.models.ratedmodel import RatedModel
from src.models.ratedobject import RatedObject
from src.models.review import Review

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
    def clean(self):
        if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
                raise forms.ValidationError("The two password fields didn't match.")
        return self.cleaned_data

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
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'signup.html', {'user_form': user_form})

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                return self.cleaned_data
            else:
                raise forms.ValidationError("Your account is disabled.")
        else:
            raise forms.ValidationError("Invalid login details supplied.")
        return self.cleaned_data

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            # authenticating twice, need to change this
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            print(login_form.errors)
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'login_form': login_form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_show(request, user_name):
    current_user = request.user
    ratedmodel_count = RatedModel.objects.filter(creator_id = current_user.userprofile.id, is_deleted = False).count()
    ratedobject_count = RatedObject.objects.filter(creator_id = current_user.userprofile.id, is_deleted = False).count()
    review_count = Review.objects.filter(userprofile_id = current_user.userprofile.id, is_deleted = False).count()
    return render(request, 'user_show.html', {'current_user': current_user, 'ratedmodel_count': ratedmodel_count,
        'ratedobject_count': ratedobject_count, 'review_count': review_count})

