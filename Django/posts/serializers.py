from rest_framework import serializers
from .models import *
from config import settings
import boto3
from botocore.exceptions import ClientError
from config.settings import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

VALID_IMAGE_EXTENSIONS = [ "jpg", "jpeg", "png", "gif", ]


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
    def validate(self, data): 
            image = data.get('thumbnail')

            if not image.name.split('.')[-1].lower() in VALID_IMAGE_EXTENSIONS: #업로드한 사진이 "jpg", "jpeg", "png", "gif"인지 확인
                serializers.ValidationError("Not an Image File")
            s3 = boto3.client('s3', #s3 객체 생성
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
                region_name = AWS_REGION)
            try:
                s3.upload_fileobj(image, AWS_STORAGE_BUCKET_NAME, image.name) #파일 업로드
                img_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{image.name}"
                data['thumbnail'] = img_url
                return data
            except:
                raise serializers.ValidationError("InValid Image File")    
   
        
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    class Meta:
        model=Comment
        fields="__all__"
        

    