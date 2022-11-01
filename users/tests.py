from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models  import User

# Create your tests here.
class UserRegistrationAPITestCase(APITestCase):
    def test_registration(self):
        url = reverse("user:signupview")
        user_data = {
            "email":"test@test.com",
            "password":"123"
        }
        # url에다가 user_data 를 넣겠다는것
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)
    # 디비가 삭제 되기 때문에 해당 test_login 은 실행이 안된다.
    # def test_login(self):
    #     url = reverse("user:token_obtain_pair")
    #     user_data = {
    #         "email":"test@test.com",
    #         "password":"123"
    #     }
    #     response = self.client.post(url, user_data)
    #     print(response.data)
    #     self.assertEqual(response.status_code, 201)

class LoginUserTest(APITestCase):
    def setUp(self):
        self.data = {'email':'test@test.com', 'password':'123'}
        self.user = User.objects.create_user('test@test.com','123')

    def test_login(self):
        response = self.client.post(reverse('user:token_obtain_pair'), self.data)
        # print(response.data['access'])
        self.assertEqual(response.status_code, 200)

    def test_get_user_data(self):
        access_token = self.client.post(reverse('user:token_obtain_pair'), self.data).data['access']
        response = self.client.get(
            path=reverse('user:signupview'),
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
            )
        # print("확인하기",response.data)
        # self.assertEqual(response.status_code, 200)
        # 로그인한 email이 저장되어있는 email 이랑 같은지 확인 하는 과정
        self.assertEqual(response.data['email'], self.data['email'])