from django import forms
from .models import Post, Comment, Communities
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=10, widget=CKEditorUploadingWidget()) # crucial field in uploading media, creates button upload
    class Meta:
        model = Post
        fields = ['title', 'text', 'category']

# class RateCommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['rate', 'author', 'post']
#         widgets = {
#             'rate': forms.Select(choices=Comment.RATE)
#         }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post', 'comment_text']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Communities
        fields = ['name', 'description', 'members']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username']

    #creates new user instance without immediately saving it(allows for modifications before saving)
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            try:
                basic_group = Group.objects.get(name='basic')#retrieves the basic group
                basic_group.user_set.add(user)#adds newly created user to this group
            except Group.DoesNotExist:
                messages.warning(self.request, "The 'basic' group does not exist. Please create it.")
        return user


# {% if messages %}
#   <ul class="messages">
#     {% for message in messages %}
#       <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
#     {% endfor %}
#   </ul>
# {% endif %}
