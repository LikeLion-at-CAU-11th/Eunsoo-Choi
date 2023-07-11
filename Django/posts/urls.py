from django.urls import path,include
from posts.views import *
from . import views
from rest_framework.routers import DefaultRouter
#as_view()를 통해서 함수 연결하는 과정을 대신 해줌!
router=DefaultRouter()
router.register('',views.PostViewSet)
urlpatterns = [
    #path('hello_world', hello_world, name = 'hello_world'),
    #path('<int:id>',post_detail,name="post_detail"),
    #path('all/',post_all,name="post_all"),
    #path('new/',create_post,name="create_post"),
    #path('comment/<int:post_id>/',get_comment,name='getcomment'),
    #path('newcomment/',create_comment,name="create_comment"),
    #path('date/',post_date,name="post_date")
    #path('',PostList.as_view()),
    path('<int:id>/',PostDetail.as_view()),
    path('com/',CommentList.as_view()),
    path('com/<int:key>/',PostCommentList.as_view()),
    path('com/<int:id>/<int:key>/',CommentDetail.as_view()),
    #path('',views.post_list),
    #path('<int:pk>/',views.post_detail_vs),
    path('',PostList.as_view()),
    path('',include(router.urls))
]