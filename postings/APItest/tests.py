from rest_framework import APITestCase
from django.contrib.auth import get_user_model

from postings.models import BlogPost

User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='toaha')
        user_obj.set_password('1234')
        user_obj.save()
        blog_post = BlogPost.object.create(
            user=user_obj,
            title='New title',
            content='some random content'
        )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)