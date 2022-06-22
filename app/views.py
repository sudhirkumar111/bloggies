from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SinUpForm, loginform,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def home(request):
    post = Post.objects.all()
    return render(request, 'app/home.html',{'post':post})

def about(request):
    return render(request, 'app/about.html')

def dashboard(request):
    if request.user.is_authenticated:
        post = Post.objects.filter(author__exact=request.user)
        user = request.user
        name = user.first_name
        return render(request, 'app/dashboard.html',{'post':post,'name':name})
    else:
       return HttpResponseRedirect('/login/')

# def user_signup(request):
#     if request.method == "POST":
#         form = SinUpForm(request.POST)
#         if form.is_valid():
#             messages.success(request, 'Congratulation !, You have Become an Author')
#             form.save()
#             return HttpResponseRedirect("/login/")
#     else:
#         form  = SinUpForm()
#     return render(request, 'app/signup.html',{'form':form})

def user_signup(request):
    if request.method == "POST":
        form = SinUpForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']            
            messages.success(request, 'Congratulation !, You have Become an Author')
            form.save()
            html_template = 'app/welcome.html'
            mydict = {'fname':fname,'lname':lname,'email':email}
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Congratulation, You have successfully registered with bloggies'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            return HttpResponseRedirect("/login/")
    else:
        form  = SinUpForm()
    return render(request, 'app/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = loginform(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Login is Successfull!!")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form  = loginform()
        return render(request, 'app/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")



def add_post(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pts = Post(title=title, desc=desc)
                pts.author=request.user
                pts.save()
                form = PostForm()
        else:
            form=PostForm()
        return render(request,'app/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect("/login/")


def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/dashboard/")
                
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'app/updatepost.html',{'form':form})


    else:
        return HttpResponseRedirect("/login/")

def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect("/dashboard/")

    else:
        return HttpResponseRedirect("/login/")



def post_detail(request,id):
    post=Post.objects.get(pk=id)
    return render(request,'app/detail.html',{'post':post})



    
    
    
