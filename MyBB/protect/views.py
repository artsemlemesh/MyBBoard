from urllib.parse import urlencode

from django.shortcuts import render
from board.models import Comment, Post
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from board.filters import PostFilter
from django.urls import reverse
class IndexView(ListView):
    model = Comment
    template_name = 'protect/index.html'
    context_object_name = 'comments'

    #retrieves a queryset of comments to display
    #filters for comments associated with posts authored by the current user-(self.request.id indicates so)
    #self.filterset-creates instance for further filtering based on user input
    #applies filters if GET parameters are present
    #returns empty queryset if no filters applied

    def get_queryset(self):
        queryset = Comment.objects.filter(post__author_id=self.request.user.id).order_by('-comment_date')
        self.filterset = PostFilter(self.request.GET, queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    #it requires the request object to handle user requests and perform actions within the view
    #even its within the class it acts as a standalone function, so we dont use self
    def delete_comment(request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return HttpResponseRedirect('/')#think about how to redirect to the same filtered page

    #another standalone view function within the class
    def accept_comment(request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        comment.status = True
        comment.save()
        return HttpResponseRedirect('/')



    # def rate_comment(request, comment_id):
    #     comment = Comment.objects.get(id=comment_id)
    #
    #     if request.method == 'POST':
    #         new_rating = int(request.POST.get('rate'))
    #         comment = Comment.objects.get(id=comment_id)
    #         comment.rate = new_rating
    #         comment.save()
    #     context = {'comment': comment}
    #     return render(request, 'protect/index.html', context)
