from .views import BlogPostRUDView, BlogPostListAPIView
from django.urls import path
from django.conf.urls import url

app_name = 'postings'

urlpatterns = [
    # path('<str:pk>', BlogPostRUDView.as_view(), name='api-postings'),
    url(r'^(?P<pk>\d+)/$', BlogPostRUDView.as_view(), name='post-rud'),
    path('', BlogPostListAPIView.as_view(), name='post-listcreate'),
]
