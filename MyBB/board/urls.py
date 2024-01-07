from django.urls import path
from .views import PostList, PostCreate, PostDetail, CommentCreate, CommentDetail, PostUpdate, CategoryListView, confirmation, register, subscribe, group_list, add_user_to_group, GroupCreate, community_chat_room
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'board'
urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_add'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_edit'),
    path('comment/', CommentCreate.as_view(), name='comment_add'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='comment_detail'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe',subscribe, name='subscribe' ),
    path('confirm/<str:confirmation_code>/', confirmation, name='confirm'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),

    path('create_group/', GroupCreate.as_view(), name='group_add'),
    path('group_list/', group_list, name='group_list'),
    path('add_user_to_group/<int:group_id>', add_user_to_group, name='add_user_to_group'),

    path('chat_room/<int:community_id>', community_chat_room, name = 'chat_room')

]