from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from .models import Post
from captcha.fields import CaptchaField


class SinUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'first_name':'First Name', 'last_name':'Last Name', 'email':'Email'}
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),'first_name':forms.TextInput(attrs={'class':'form-control'}),'last_name':forms.TextInput(attrs={'class':'form-control'}),'email':forms.EmailInput({'class':'form-control'}),
        }



class loginform(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=("Password"), strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    captcha = CaptchaField()
   

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','desc']
        labels = {'title':'Title', 'desc':'Description'}
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),
        'desc':forms.Textarea(attrs={'class':'form-control '})}


class ShareForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}),max_length=50)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    to = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    comments = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),required='Fasle')