from .views import register, user_login, user_logout, home, profile_view
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import (
    CommentDeleteView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    posts_by_tag,
    PostListView,
    edit_comment,
    add_comment,
    search
)

urlpatterns = [
    path('', home, name='home'), 
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('posts/', PostListView.as_view(), name='home'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:post_id>/comments/new/', add_comment, name='add-comment'),
    path('comments/<int:comment_id>/edit/', edit_comment, name='edit-comment'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete-comment'),
    path('search/', search, name='search'),
    path('tags/<str:tag_name>/', posts_by_tag, name='posts-by-tag'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)