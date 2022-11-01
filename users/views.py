from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from users import serializers
from users.models import User
from users.serializers import UserSerializer,CustomTokenObtainPairSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import get_object_or_404

# Create your views here.
class ProfileView(APIView):
    # 로그인 안해도 모든 프로필은 볼 수 있게 설정
    def get (sefl, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

class UserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class FollowView(APIView):
    def post (self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.followers.all():
            you.followers.remove(me)
            return Response("unfollow 했습니다", status=status.HTTP_200_OK)
        else:
            you.followers.add(me)
            return Response("follow 했습니다.", status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class MockView(APIView):
    # 로그인 되어있을때만 가능하게끔 설정함
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        print(request.user)
        # 어드민 권한을 주는 부분 하지만 이부분은 디비가 변경되는 부분으로 post 방식이 옳바르다
        # user = request.user
        # user.is_admin = True
        # user.save()
        return Response("get 요청")

