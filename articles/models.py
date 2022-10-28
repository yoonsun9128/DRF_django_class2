from turtle import title
from unittest.util import _MAX_LENGTH
from django.db import models
from users.models import User

# Create your models here.
class Article(models.Model):
    # 유저 삭제하면 게시물 삭제하게 설정함
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    img = models.ImageField(upload_to = '%Y/%m/')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)