from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #모든 필드를 받아주는것 __all__
        fields = '__all__'

        #비밀번호 햇싱 해주는 과정
    def create(self, validated_data):
        user = super().create(validated_data)
        print(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, validated_data):
        user = super().update(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token
