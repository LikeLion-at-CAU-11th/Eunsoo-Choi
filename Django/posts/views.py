from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import  *
from django.db import models
import json
import datetime

from .serializers import *
# 아래는 APIView를 사용하기 위해
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #상태도 받아야하니까
from django.http import Http404

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공!',
            'data' : "Hello world",
        })

@require_http_methods(["GET","PATCH","DELETE"])
def post_detail(request,id):
    if request.method == "GET":
        post=get_object_or_404(Post,pk=id)
        category_json={
            "id":post.post_id,
            "writer":post.writer,
            "content":post.content,
            "category":post.category,
        }
    
        return JsonResponse({
            'status':200,
            'message':'게시글 조회 성공',
            'data':category_json
        })
    elif request.method =="PATCH":
        body=json.loads(request.body.decode('utf-8'))
        update_post=get_object_or_404(Post,pk=id)
        
        update_post.content=body['content']
        update_post.category=body['category']
        update_post.save()
        
        update_post_json={
            "id":update_post.post_id,
            "writer":update_post.writer,
            "content":update_post.content,
            "category":update_post.category,
        }
        return JsonResponse({
            'status':200,
            'message':'게시글 수정 성공',
            'data':update_post_json
        })
    elif request.method =="DELETE":
        delete_post=get_object_or_404(Post, pk=id)
        delete_post.delete()
        
        return JsonResponse({
            'status':200,
            'message':'게시글 삭제 성공',
            'data':None
        })
@require_http_methods(["GET"])
def post_all(request): 
    posts=Post.objects.all()
    category_list=[]
    
    for post in posts:
        category_list.append({
            
        "id":post.post_id,
        "writer":post.writer,
        "content":post.content,
        "category":post.category,
            
        })
    return JsonResponse({
        'status':200,
        'message':'모든 게시글 조회 성공',
        'data':category_list
    })
    
@require_http_methods(["POST"])
def create_post(request):
    body=json.loads(request.body.decode('utf-8'))
    
    new_post=Post.objects.create(
        writer=body['writer'],
        content=body['content'],
        category=body['category']
    )
    
    new_post_json={
        "id":new_post.post_id,
        "writer":new_post.writer,
        "content":new_post.content,
        "category":new_post.category
    }
    return JsonResponse({
        'status':200,
        'message':'게시글 목록 조회 성공',
        'data': new_post_json
    })
@require_http_methods(["GET"])
def get_comment(request,post_id):
    comments=Comment.objects.filter(post=post_id)
    comment_json_list=[]
    for comment in comments:
        commet_json={
            'writer':comment.writer,
            'content':comment.content
        }
        comment_json_list.append(commet_json)
        
    return JsonResponse({
        'status':200,
        'message':'댓글 읽어오기 성공',
        'data':comment_json_list
    })
    
@require_http_methods(["POST"])
def create_comment(request):
    body=json.loads(request.body.decode('utf-8'))
    
    comment_post_id=Post.objects.get(post_id=body["post_id"])
    
    new_comment=Comment.objects.create(
        post=comment_post_id,
        writer=body["writer"],
        content=body["content"]
    )
    
    new_comment_json={
        "post":body["post_id"], #왜 new_comment.post, comment_post_id로 하면 안되는 걸까요ㅠㅜ
        "writer":new_comment.writer,
        "content":new_comment.content,
    }
    
    return JsonResponse({
        'status': 200,
        'message':'댓글 생성 성공',
        'data':new_comment_json
    })
    
    
@require_http_methods(["GET"])
def post_date(request): 
    start=datetime.date(2023,4,5)
    end=datetime.date(2023,4,11)
    posts=Post.objects.filter(created_at__range=(start,end))
    post_list=[]
    
    for post in posts:
        post_list.append({
            "id":post.post_id,
            "writer":post.writer,
            "content":post.content,
            "category":post.category
        })
    
    return JsonResponse({
        'status':200,
        'message':'5주차~6주차 게시글 조회 성공',
        'data':post_list
    })
    
#보통 리스트에는 get, post가 들어감.
class PostList(APIView) :
    #게시글 새로 만들기
    def post(self,request,format=None):
        serializer = PostSerializer(data=request.data) #요청받은 데이터를 데이터에 넣고, 이걸 포스트시리얼라이저에 정렬
        if serializer.is_valid(): #유효하고 검증된 값인지
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    #모든 게시글 정보 가져오기
    def get(self,request,format=None):
        posts=Post.objects.all()
        #많은 post를 받아오려면 many=true 써줘야 에러 안남
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    
class PostDetail(APIView):
    def get(self, request,id):
        post=get_object_or_404(Post,id=id)
        serializer=PostSerializer(post)
        return Response(serializer.data)
    #put은 전체 바꾸기 patch는 일부분
    def put(self,request,id):
        post=get_object_or_404(Post,id=id) #객체가 존재하지 않을때 http404 에러를 발생시킴
        serializer=PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        post=get_object_or_404(Post,id=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#댓글 전체리스트 가져오기
class CommentList(APIView):
    def get(self,request,format=None):
        comments=Comment.objects.all()
        serializer=CommentSerializer(comments,many=True)
        return Response(serializer.data)

#글을 중심으로 가져오기
class PostCommentList(APIView):
    #글 번호를 이용하여 특정 글의 댓글 전체 가져오기
    def get(self,request,key,format=None):
        #comments=get_object_or_404(Comment,post=key)
        comments=Comment.objects.filter(post=key)
        serializers=CommentSerializer(comments,many=True)
        return Response(serializers.data)
    
    #글 번호를 이용하여 특정 글에 댓글 생성하기
    def post(self,request,key):
        commentPost=Post.objects.get(id=key)
        data=request.data
        data["post"]=key        
        serializer=CommentSerializer(data=data)
        #serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["post"]=commentPost
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

#글 번호와 댓글 번호를 이용하여 조회, 수정, 삭제하기
class CommentDetail(APIView):          
    def get(self,request,id,key):
        comment=get_object_or_404(Comment,id=id,post=key)
        serializer=CommentSerializer(comment)
        return Response(serializer.data)
    
    def put(self,request,id,key):
        comment=get_object_or_404(Comment,id=id,post=key)
        serializer=CommentSerializer(comment,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id,key):
        comment=get_object_or_404(Comment,id=id,post=key)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
from rest_framework import generics
from rest_framework import mixins
#mixins은 apiview에서 request method마다 serializer 처리할때 중복되는 과정을 줄여줄 수 있다.
#List/Create/Retrieve/Update/Destroy+ModelMixin = 리스팅,생성+저장,모델인스턴스 돌려주기, 업데이트+저장, 삭제
#보통 genericApiView와 결합하여 crud를 구현한다.
#mixin 클래스 안에 존재하는 것과 같은 클래스 이름 쓸 경우 오버라이딩될 수 있으니 주의!!! 이름 신중하게 지을것!

class PostListMixins(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    #아래 두줄처럼 queryset, serializer_class 지정해줘야함.
    queryset = Post.objects.all()
    serializer_class=PostSerializer
    
    def get(self,request,*args,**kwargs):
        return self.list(request)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class PostDetailMixins(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset= Post.objects.all()
    serializer_class=PostSerializer
    def get(self,request,*args,**kwargs):
        return self.retrieve(request)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
    
#mixin 여러개 상속해야하기 때문에 concrete generic views 사용하면 가독성 좋아짐
# ex) createAPIView는 genericAPIView, CreateModelMixin 상속받음. 
class PostListGenericAPIView(generics.ListCreateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    
class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    
from rest_framework import viewsets
#viewset에서는 urls 말고 여기에 as_view()
#코드 간소화 방법
#queryset과 serializer 한번에 처리 가능

# ReadOnlyModelViewSet : 목록/특정 레코드 조회 => 속도 측면에서 좋음. 
# ModelViewSet이 보통 많이 쓰임. 
class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    
#post_list = PostViewSet.as_view({
#    'get':'list',
#    'post':'create',
#})
#post_detail_vs = PostViewSet.as_view({
#    'get':'retrieve',
#    'put':'update',
#    'patch':'partial_update',
#    'delete':'destroy',
#})

    