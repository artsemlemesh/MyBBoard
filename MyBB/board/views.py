from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Post, Comment, DisposableCode, Category, Communities, Message
from .forms import PostForm, CommentForm, MyUserCreationForm, GroupForm
import secrets
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.paginator import Paginator

class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    #form_valid assigns current logged in user to be an author of the post (usually for create or update views)

    def form_valid(self, form):
        post = form.save(commit=False) #Creates a new post object from the form data, but doesn't save it to the database yet.This allows for additional modification
        form.instance.author = self.request.user #(Setting author) assighns current log-in user as the author of the post
        post.save() #commits the post object to the database
        return super().form_valid(form)#calling superclass of the parent (CreateView) , which handles: Redirecting user to a success url, setting a success message in the session

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'





class CommentCreate(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_create.html'

    #form_valid assigns current logged-in user to be an author of the comment (usually for create or update views)
    def form_valid(self, form):
        comment = form.save(commit=False)
        form.instance.author = self.request.user
        comment.save()
        return super().form_valid(form)

class GroupCreate(CreateView):
    form_class = GroupForm
    model = Communities
    template_name = 'group/group_create.html'


class CommentDetail(DetailView):
    model = Comment
    template_name = 'comment.html'
    context_object_name = 'comment'


class CategoryListView(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_list'

    #by clicking on a certain category it filters it and returns only posts belonging to a selected category
    def get_queryset(self, *args, **kwargs):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            disposable_code = DisposableCode.objects.create(user=user, code=generate_unique_code())
            send_confirmation_email(user, disposable_code.code)
            user.is_active = False
            user.save()
            return HttpResponseRedirect('/')
    else:
        form = MyUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# def create_group(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         group = Communities.objects.create(name=name, description=description)
#         group.members.add(request.user)
#         return redirect('board:group_list')
#     else:
#         return render(request, 'group/create_group.html')


def group_list(request):
    groups = Communities.objects.all()
    return render(request, 'group/group_list.html', {'groups':groups})

@login_required
def add_user_to_group(request, group_id):
    group = Communities.objects.get(id=group_id)#fetches a specific group from the db

    if request.method == 'POST': #checks if the user has submitted a form (like clicking the 'save' button), if so it processess the data
        selected_user_ids = request.POST.getlist('user_id')  # grabs a list of user IDs from the submitted form data
        for user_id in selected_user_ids:
            try: #this block tries to find the user with the given ID
                user_id = int(user_id)
                user = User.objects.get(id=user_id)
                group.members.add(user)
            except User.DoesNotExist:
                return redirect('board:group_list')
        else:
            return redirect(reverse('board:add_user_to_group', args=([group_id])))

    else: # if it wasnt form submission (usually a first-time visit), this part runs
        all_users = User.objects.exclude(communities=group)  # Exclude existing members
        context = {'group': group, 'all_users': all_users}
        return render(request, 'group/add_user_to_group.html', context)




# def community_chat_room(request, community_id):
#     community = get_object_or_404(Communities, pk=community_id)
#     if request.user not in community.members.all():
#         return HttpResponseForbidden('You are not a member')
#
#     if request.method == 'POST':
#         message_text = request.POST.get('message')
#         if message_text:
#             message = Message.objects.create(user=request.user, community=community, content=message_text)
#             return redirect('board:chat_room', community_id=community_id)  # Redirect after POST
#         else:
#             return JsonResponse({'error': 'Empty message'})
#
#     # GET request or empty message: fetch and display messages
#     messages = Message.objects.filter(community=community).order_by('-timestamp')
#     paginator = Paginator(messages, 5)  # 10 messages per page
#     page_number = request.GET.get('page')# PAGINATION DOESNT WORK PROPERLY
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'messages/chat_room.html', {'community': community, 'messages': messages, 'page_obj': page_obj})



def send_message(request, community_id):#THIS VIEW ISNT CONNECTED TO URLS AND I NEED TO FIGURE OUT WHAT IT IS FOR
    community = get_object_or_404(Communities, pk=community_id)
    if request.user not in community.members.all():
        return JsonResponse({'error': 'Not a member'})
    message_text = request.POST.get('message')
    if message_text:
        message = Message.objects.create(
            user=request.user, community=community, content=message_text
        )
        # Fetch new messages for real-time updates (long polling)
        new_messages = Message.objects.filter(community=community, timestamp__gt=message.timestamp)
        return JsonResponse({'messages': list(new_messages.values())})  # Return new messages
    else:
        return JsonResponse({'error': 'Empty message'})






def generate_unique_code():
    while True:
        code = secrets.token_urlsafe(10)
        if not DisposableCode.objects.filter(code=code).exists():
            break
    return code


def send_confirmation_email(user, confirmation_code):
    subject = 'account confirmation email'
    message = f'Hello {user.username}, \n\nPlease confirm your registration by clicking the following link:\n\nhttp://127.0.0.1:8000/board/confirm/{confirmation_code}'
    send_mail(subject, message, ['noreply@example.com'], [user.email])





def confirmation(request, confirmation_code):
    try:
        disposable_code = DisposableCode.objects.get(code=confirmation_code)
        disposable_code.user.is_active = True
        disposable_code.user.save()
        disposable_code.delete()
        return render(request, 'registration/confirmation_success.html')
    except DisposableCode.DoesNotExist:
        return render(request, 'registration/confirmation_error.html')

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    print(f'category: {category}')################################
    message = 'you have successfully subscribed to the category: '
    return render(request, 'subscribe.html', {'category':category, 'message': message})


# defference in work of GET and POST requests
#GET request users query string to send the data, after ? symbol: (e.g., https://example.com/search?q=cats).
#POST request send data in the request body, hidden from the url