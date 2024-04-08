from django.contrib.syndication.views import Feed
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Book, Customer
from .serializers import BookSerializer


class BookListView(ListView):
    template_name = 'books/book-list.html'
    model = Book
    context_object_name = 'books'
    ordering = 'title'

    def get_queryset(self):
        return self.model.objects.all()


class BookDetailView(DetailView):
    template_name = 'books/book-detail.html'
    model = Book
    context_object_name = 'book'

    def get_queryset(self):
        return self.model.objects.all()

    def mark_as_read(request, item_id):
        item = get_object_or_404(Book, id=item_id)
        item.is_read = True
        item.save()
        return JsonResponse({'message': 'Item marked as read'})

    def add_to_favorites(request, item_id):
        item = get_object_or_404(Book, id=item_id)
        item.is_favorite = True
        item.save()
        return JsonResponse({'message': 'Item added to favorites'})


class DjangoFilterBackend:
    pass


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['title', 'author']

    def list(self, request, *args, **kwargs):
        data = list(Book.objects.all().values())
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        data = list(Book.objects.filter(id=kwargs['pk']).values())
        return Response(data)

    def create(self, request, *args, **kwargs):
        book_serializer = BookSerializer(data=request.data)
        if book_serializer.is_valid():
            book_serializer.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Book added sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "please fill the details", "status": status_code})

    def destroy(self, request, *args, **kwargs):
        book_data = Book.objects.filter(id=kwargs['pk'])
        if book_data:
            book_data.delete()
            return Response({"message": "Book deleted sucessfully", "status": status.HTTP_204_NO_CONTENT})
        else:
            return Response({"message": "Book not found", "status": status.HTTP_404_NOT_FOUND})

    def update(self, request, *args, **kwargs):
        book_data = Book.objects.filter(id=kwargs['pk'])
        book_data_serializer = BookSerializer(book_data, data=request.data)
        if book_data_serializer.is_valid():
            book_data_serializer.save()
            return Response({"message": "Book updated sucessfully", "status": status.HTTP_200_OK})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Book not found", "status": status_code})


class LatestBookFeed(Feed):
    title = 'Latest Books'
    link = reverse_lazy('books:book-list')
    description = 'List of latest books'

    def items(self):
        return Book.objects.all()

    def item_title(self, item: Book):
        return item.title

    def item_link(self, item: Book):
        return reverse('books:book-detail', kwargs={'pk': item.pk})

