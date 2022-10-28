from ast import Delete
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# 게시글 보여주기 등록하기
class ArticlesView(APIView):
    def get (self, request):
        pass
    def post (self, request):
        pass

# 게시글 상세페이지 및 수정 삭제
class ArticleDetailView(APIView):
    def get (self, request, article_id):
        pass
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