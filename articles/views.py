
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from articles.models import Article
from articles.serializers import ArticleSerializer, ArticleListSerializer, ArticleCreateSerializer

# 게시글 보여주기 등록하기
class ArticlesView(APIView):
    def get (self, request):
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post (self, request):
        print(request.user)
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)

# 게시글 상세페이지 및 수정 삭제
class ArticleDetailView(APIView):
    def get (self, request, article_id):
        article = Article.objects.get(pk=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    def put (self, request, article_id):
        pass
    def delete (self, request, article_id):
        pass

# 댓글창
class CommnetView(APIView):
    def get (self, request, article_id):
        pass
    def post (self, request, article_id):
        pass

# 댓글 수정 삭제
class CommentDetailView(APIView):
    def put (self, request, commnet_id):
        pass
    def delete (self, request, commnet_id):
        pass

# 좋아요 카운트
class LikeView(APIView):
    def post (self, request):
        pass