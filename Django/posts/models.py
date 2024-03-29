from django.db import models
from accounts.models import *


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract = True

class Post(BaseModel):

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )
    
    # 수정 전 post_id // model 바꾸면 makemigrations -> migrate 하기
    id = models.AutoField(primary_key=True)
    #writer = models.CharField(verbose_name="작성자", max_length=30)
    writer = models.ForeignKey(Member,on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    category = models.CharField(choices=CHOICES, max_length=20)
    #모델에 사진 추가
    thumbnail=models.ImageField(verbose_name="썸네일", null=True)
 

class Comment(BaseModel):
    writer = models.CharField(verbose_name="작성자", max_length=30)
    content = models.CharField(verbose_name="내용", max_length=200)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, blank=False)