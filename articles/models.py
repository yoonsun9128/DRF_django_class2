from django.db import models
from users.models import User
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    # 유저 삭제하면 게시물 삭제하게 설정함
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    img = models.ImageField(null=True, upload_to = '%Y/%m/')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # related_name을 설정해줘서 다른 필드 부분과 곁치는걸 방지하기 위해
    likes = models.ManyToManyField(User, related_name="like_articles")

    def get_absolute_url(self):
        return reverse('articles:Article_detail', kwargs={'article_id':self.id})

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)