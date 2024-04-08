from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BookListView, BookDetailView, BookViewSet, LatestBookFeed


app_name = 'books'
router = DefaultRouter()
router.register('books', BookViewSet, basename='books')



urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('feed/', LatestBookFeed(), name='book-feed'),
]