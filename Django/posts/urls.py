from django.urls import path
from posts.views import *

urlpatterns = [
    #path('hello_world', hello_world, name = 'hello_world'),
    #path('<int:id>',post_detail,name="post_detail"),
    #path('all/',post_all,name="post_all"),
    #path('new/',create_post,name="create_post"),
    #path('comment/<int:post_id>/',get_comment,name='getcomment'),
    #path('newcomment/',create_comment,name="create_comment"),
    #path('date/',post_date,name="post_date")
    path('',PostList.as_view()),
    path('<int:id>/',PostDetail.as_view()),
    path('com/',CommentList.as_view()),
    path('com/<int:id>/',CommentDetail.as_view()),
    
]