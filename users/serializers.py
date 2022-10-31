from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User
from articles.serializers import ArticleListSerializer

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

class UserProfileSerializer(serializers.ModelSerializer):
    # 아이디값으로 보임
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 이메일 값으로 보임
    # followers = serializers.StringRelatedField(many=True)
    # 작성한 글 띄우기
    article_set = ArticleListSerializer(many=True)
    # 유저가 좋아요한 글 보이기
    like_articles = ArticleListSerializer(many=True)
    class Meta:
        model = User
        fields = ("id", "email", "followings", "followers", "article_set", "like_articles")

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token
