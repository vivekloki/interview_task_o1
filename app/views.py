from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q  # Import Q for complex queries
from .models import BooksBook
from .serializers import BooksBookSerializer

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookListView(generics.ListAPIView):
    queryset = BooksBook.objects.prefetch_related('booksbookauthors_set', 'booksbookbookshelves_set', 'booksbooklanguages_set', 'booksbooksubjects_set', 'booksformat_set')
    serializer_class = BooksBookSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        book_id = self.request.query_params.get('book_id', None)
        if book_id is not None:
            # Filter queryset based on Book ID
            queryset = queryset.filter(id=book_id)
        return queryset