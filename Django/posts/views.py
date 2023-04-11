from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import  *
from django.db import models
import json
import datetime
# Create your views here.

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