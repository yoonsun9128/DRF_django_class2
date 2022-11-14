from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from articles.models import Article
from users.models  import User
from faker import Faker
from articles.serializers import ArticleSerializer
# 이미지 업로드 확인(임시파일로 불러다가 할예정=tempfile)
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new('RGBA', size, color)
    image.save(temp_file,'png')
    return temp_file

# Create your tests here.
class ArticleCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'email':'test@test.com','password':'123'}
        cls.article_data = {'title':'some title', 'content':'some content'}
        cls.user = User.objects.create_user('test@test.com','123')

    def setUp(self):
        self.access_token = self.client.post(reverse('user:token_obtain_pair'), self.user_data).data['access']

    # setup은 매번 할때 지정
    # def setUp(self):
    #     self.user_data = {'email':'test@test.com','password':"123"}
    #     self.article_data = {'title':'some title', 'content':'some content'}
    #     self.user = User.objects.create_user('test@test.com','123')
    #     self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']

    # 로그인인 안한 상태에서 401 에러 작동
    def test_fail_if_not_logged_in(self):
        url = reverse('articles:article')
        response = self.client.post(url, self.article_data)
        self.assertEqual(response.status_code, 401)
    def test_create_article(self):
        response = self.client.post(
            path=reverse('articles:article'),
            data=self.article_data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 200)

def test_create_article_with_image(self):
    # 임시 이미지 파일 생성
    temp_file = tempfile.NamedTemporaryFile()
    temp_file.name = 'image.png'
    image_file = get_temporary_image(temp_file)
    # 이미지의 첫번째 프레임 받아오기
    image_file.seek(0)
    self.article_data['image'] = image_file

    # 전송
    response = self.client.post(
            path=reverse('articles:article'),
            data=encode_multipart(data = self.article_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
    self.assertEqual(response.status_code, 200)

class ArticleReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.articles=[]
        # 10명의 유저가 각각 하나의 게시글을 쓰는형식으로 짬(이건 for 문을 어떻게 짜냐에 따라 다름)
        for i in range(10):
            cls.user=User.objects.create_user(cls.faker.name(), cls.faker.word())
            cls.articles.append(Article.objects.create(title=cls.faker.sentence(), content=cls.faker.text(),user=cls.user))

    def test_get_article(self):
        for article in self.articles:
            url = article.get_absolute_url()
            response = self.client.get(url)
            # 돌아오는 response 값이랑 비교하기 위해 serializer 를 넣어줌
            serializer = ArticleSerializer(article).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)
                print(key, value)

