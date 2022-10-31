from rest_framework import serializers
from articles.models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.email
    class Meta:
        model = Comment
        exclude = ("article",)

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields 안에 하나의 인자값만 넣을 경우 꼭 마지막에 ,를 넣어야 한다. 넣지 않으면 string으로 받아드려서 오류남
        fields = ('content',)

class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True)
    # 좋아요 한 부분은 pk 값아닌 이메일값으로 보이게 하기
    likes = serializers.StringRelatedField(many=True)
    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Article
        fields = '__all__'

# 포스트맨에서 유저 값을 로그인 토큰을 이용해도 등록되지 않아 우선 직접 적을 수 있는 부분만 다시 시리얼라이즈 모델 만듬
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "content", "img")

# 받고 싶은 필드 설정하고 싶을때
class ArticleListSerializer(serializers.ModelSerializer):
    # 폴인키값말고 유저 이메일로 보여주기 위해
    user = serializers.SerializerMethodField()
    # 좋아요 수
    like_count = serializers.SerializerMethodField()
    # 댓글 수
    comment_count = serializers.SerializerMethodField()
    # obj=article(게시글이다)
    def get_user(self, obj):
        return obj.user.email

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self,obj):
        return obj.comment_set.count()
    class Meta:
        model = Article
        fields = ("pk", "title", "img", "update_at", "user", "like_count", "comment_count")
