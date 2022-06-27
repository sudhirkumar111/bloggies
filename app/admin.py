from django.contrib import admin
from .models import Post, Comment, Contact

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','desc','create','update']



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on')
    
@admin.register(Contact)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','comment')
    

