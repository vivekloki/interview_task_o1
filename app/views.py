from django.db.models import Q
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
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
        filters = {}

        # Book ID numbers specified as Project Gutenberg ID numbers
        book_ids = self.request.query_params.get('book_ids')
        if book_ids:
            filters['gutenberg_id__in'] = book_ids.split(',')

        # Language
        languages = self.request.query_params.get('language')
        if languages:
            filters['booksbooklanguages_set_languagecode_in'] = languages.split(',')

        # Mime-type
        mime_types = self.request.query_params.get('mime_type')
        if mime_types:
            filters['booksformat_set_mime_type_in'] = mime_types.split(',')

        # Topic (subject or bookshelf) - Case-insensitive partial matches
        topic = self.request.query_params.get('topic')
        if topic:
            filters['$or'] = [
                {'booksbooksubjects_set_subjectname_icontains': topic},
                {'booksbookbookshelves_set_bookshelfname_icontains': topic},
            ]

        # Author - Case-insensitive partial matches
        author = self.request.query_params.get('author')
        if author:
            filters['booksbookauthors_set_authorname_icontains'] = author

        # Title - Case-insensitive partial matches
        title = self.request.query_params.get('title')
        if title:
            filters['title__icontains'] = title

        return queryset.filter(**filters)