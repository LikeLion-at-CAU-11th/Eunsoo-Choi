from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post
from django.db import models
import json
# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공!',
            'data' : "Hello world",
        })

@require_http_methods(["GET"])
def get_post_detail(request,id):
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
    
@require_http_methods(["GET"])
def get_post_all(request): 
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
    