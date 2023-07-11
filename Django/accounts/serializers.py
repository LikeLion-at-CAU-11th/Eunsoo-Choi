# accounts/serializers.py
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import Member

# accounts/serializers.py
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = Member
        fields = ['username', 'password']
    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if Member.objects.filter(username=username).exists():
            member = Member.objects.get(username=username)
		        
			# DB에 해당 데이터가 존재하는데 password가 일치하지 않는 경우
            if not member.check_password(password):
                raise serializers.ValidationError("wrong password")
        else:
            raise serializers.ValidationError("member account not exist")
        
        token = RefreshToken.for_user(member)
        refresh_token = str(token)
        access_token = str(token.access_token)
        data = {
				    'member':member,
				    'refresh_token':refresh_token,
				    'access_token':access_token,
		}
        return data
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)

    class Meta:
        model = Member
        fields = ['id', 'password', 'username', 'email', 'age']
            
    
    def save(self, request):

       member = Member.objects.create(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            age=self.validated_data['age'],
        )
       member.set_password(self.validated_data['password'])
       member.save()
       return member
    
		# password 암호화
  
        

        
    
    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)

        if Member.objects.filter(email=email).exists():
            raise serializers.ValidationError('email already exists')
        if Member.objects.filter(username=username).exists():
            raise serializers.ValidationError('username already exists')
        
        return data
    
    