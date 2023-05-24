from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        # 어떤 모델을 시리얼라이즈 할건지
        model = Post
        # 모델에서 어떤 필드를 가져올지
        # 전부 가져오고 싶을때
        fields="__all__"
      
     #추가
        #가져올 필드를 지정해 줄수도 있다.
        #fields = ['writer','content']
        
        #제외할 필드 지정
        # exclude =['id']   
        
        #create,update,delete 는 불가능하고 read만되는 필드 선언
        #속도가 빨라지는 장점이 있음
        #read_only_fields=['writer']
        
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    class Meta:
        model=Comment
        fields="__all__"
        

    