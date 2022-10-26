from rest_framework import serializers
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
