from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status

from rest_framework_jwt.settings import api_settings

from postings.models import BlogPost

User = get_user_model()
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER
class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='toaha')
        user_obj.set_password('1234')
        user_obj.save()
        blog_post = BlogPost.objects.create(
            user=user_obj,
            title='New title',
            content='some random content'
        )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_get_list(self, request=None):
        data        = {}
        blog_post   = BlogPost.objects.first()
        url         = api_reverse("api-postings:post-listcreate", request=request)
        # url       = blog_post.get_api_url()

        # print(url)
        response    = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data        = {"title": "no title", "content": "no content"}
        # url       = BlogPost.objects.first()
        url         = api_reverse("api-postings:post-listcreate")
        response    = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        data        = {}
        blogpost    = BlogPost.objects.first()
        url         = blogpost.get_api_url()
        response    = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_item(self):
        data        = {"title": "no random title", "content": "no random content"}
        blogpost    = BlogPost.objects.first()
        url         = blogpost.get_api_url()
        response    = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response    = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        user_obj    = User.objects.first()
        payload     = payload_handler(user_obj)
        token_rsp   = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        data        = {"title": "no random title", "content": "no random content"}
        blogpost    = BlogPost.objects.first()
        url         = blogpost.get_api_url()
        response    = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item_with_user(self):
        user_obj    = User.objects.first()
        payload     = payload_handler(user_obj)
        token_rsp   = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        data        = {"title": "no random title", "content": "no random content"}
        url         = api_reverse("api-postings:post-listcreate")
        response    = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(username='testuser1')
        blog_post = BlogPost.objects.create(
            user=owner,
            title='New title',
            content='some random content'
        )

        user_obj    = User.objects.first()
        payload     = payload_handler(user_obj)
        token_rsp   = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        print(token_rsp)
        data        = {"title": "no random title", "content": "no random content"}
        url         = blog_post.get_api_url()
        response    = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data        = {
            'username': 'toaha',
            'password': '1234'
        }
        url         = api_reverse("api-login")
        response    = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token       = response.data.get("token")
        print(token, url)
        if token is not None:
            blog_post   = BlogPost.objects.first()
            url         = blog_post.get_api_url()
            data        = {"title": "some random title", "content": "some random content"}
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response    = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            print(url, response)