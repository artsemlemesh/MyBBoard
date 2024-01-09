from django.contrib import admin
from .models import Post, PostCategory, Category, Comment, Communities, Message, PostComment

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Category)
admin.site.register(Communities)
admin.site.register(Message)
admin.site.register(PostComment)
