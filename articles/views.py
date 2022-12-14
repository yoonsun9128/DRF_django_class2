from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from articles.models import Article, Comment
from django.db.models import Q
from articles.serializers import ArticleSerializer, ArticleListSerializer, ArticleCreateSerializer, CommentSerializer, CommentCreateSerializer

# 게시글 보여주기 등록하기
class ArticlesView(APIView):
    def get (self, request):
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post (self, request):
        print(request.user)
        if not request.user.is_authenticated:
                return Response({"message":"로그인 해주세요"}, 401)
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세페이지 및 수정 삭제
class ArticleDetailView(APIView):
    def get (self, request, article_id):
        # article = Article.objects.get(pk=article_id)
        article= get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put (self, request, article_id):
        article= get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 본인 또는 운영자인지 확인 에러/401은 로그인이 되었는지에 대한 에러
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

    def delete (self, request, article_id):
        article= get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response("삭제되었음!", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

# 댓글창
class CommnetView(APIView):
    # 리스트 보이기
    def get (self, request, article_id):
        article = Article.objects.get(id=article_id)
        commnets = article.comment_set.all()
        serializer = CommentSerializer(commnets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post (self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 댓글 수정 삭제
class CommentDetailView(APIView):
    def put (self, request, article_id, commnet_id):
        comment= get_object_or_404(Comment, id=commnet_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 본인 또는 운영자인지 확인 에러/401은 로그인이 되었는지에 대한 에러
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)
    def delete (self, request, article_id, commnet_id):
        comment= get_object_or_404(Comment, id=commnet_id)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제되었음!", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

# 좋아요 카운트
class LikeView(APIView):
    def post (self, request, article_id):
        article= get_object_or_404(Article, id=article_id)
        print(article.likes)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("좋아요 취소 되었습니다", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("좋아요 눌렀습니다.", status=status.HTTP_200_OK)

# 내가 팔로우한 사람의 게시물만 보기 위해
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        q = Q()
        for user in request.user.followings.all():
            q.add(Q(user=user), q.OR)
        feeds = Article.objects.filter(q)
        serializer = ArticleListSerializer(feeds, many=True)
        return Response(serializer.data)
        pass