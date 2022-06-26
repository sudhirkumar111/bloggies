from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SinUpForm, loginform,PostForm,ShareForm,CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post,Comment

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

# Create your views here.
def home(request):
    post = Post.objects.all()   
    return render(request, 'app/home.html',{'post':post,})

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
            
            form.save()
            messages.success(request, 'Congratulation !, You have Become an Author')
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
    form = CommentForm()
  
    if request.method == 'POST':
        data = CommentForm(request.POST)
        if data.is_valid():
                newdata = data.save(commit=False)
                newdata.post=post
                newdata.save()
                return HttpResponseRedirect('/')
               
        else:
            form = CommentForm() 
        return render(request, 'app/detail.html',{'form':form})
    
    else:
           
        comment = post.comments.all()
        
        form = CommentForm()
        return render(request,'app/detail.html',{'form':form,'post':post,'comment':comment})

def postshare(request,id):
    post =Post.objects.get(pk=id)
    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],post.title)
            message='Read Post at: \n {}\n\n{}\'s Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            mg = EmailMessage(subject,message,'connect.sudhirkumar@gmail.com',[cd['to']])
            # print(post_url) 
            mg.send()     
            return render(request,'app/sharemsg.html')       
            
        else:
            return HttpResponseRedirect('/')

        
    
    else:
        form = ShareForm()
        return render(request,'app/postshare.html',{'form':form})



# def PostComment(request,id):
#     comment = comment.objects.get(pk=id)
#     return render(request,'app/detail.html',{'comment':comment})
    
    
    
