from rest_framework import serializers
from articles.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "content", "img")

# 받고 싶은 필드 설정하고 싶을때
class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # obj=article(게시글이다)
    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Article
        fields = ("pk", "title", "img", "update_at", "user")