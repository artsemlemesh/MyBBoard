from django_filters import FilterSet, ModelChoiceFilter
from .models import Comment, Post

#this class designed to filter comments based on a specific user's post

class PostFilter(FilterSet):
    #creates a filter named post for filtering comments based on the associated post using a dropdown menu
    post = ModelChoiceFilter(
        empty_label='all posts',
        field_name='post',
        label='filter',
        queryset=Comment.objects.all()
    )

    class Meta:
        model = Comment
        fields = ('post',)

    #to achieve this filtering, __init__ modifies default queryset to the post filter
    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(author_id=kwargs['request'])