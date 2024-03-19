from rest_framework import serializers
from .models import BooksBook, BooksBookAuthors, BooksAuthor, BooksBookshelf, BooksBookBookshelves, BooksBookLanguages, BooksBookSubjects, BooksLanguage, BooksSubject, BooksFormat

class BooksAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksAuthor
        fields = ['name', 'birth_year', 'death_year']

class BooksBookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBookshelf
        fields = ['name']

class BooksLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksLanguage
        fields = ['code']

class BooksSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksSubject
        fields = ['name']

class BooksFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksFormat
        fields = ['mime_type', 'url']

class BooksBookAuthorsSerializer(serializers.ModelSerializer):
    author = BooksAuthorSerializer()

    class Meta:
        model = BooksBookAuthors
        fields = ['author']

class BooksBookBookshelvesSerializer(serializers.ModelSerializer):
    bookshelf = BooksBookshelfSerializer()

    class Meta:
        model = BooksBookBookshelves
        fields = ['bookshelf']

class BooksBookLanguagesSerializer(serializers.ModelSerializer):
    language = BooksLanguageSerializer()

    class Meta:
        model = BooksBookLanguages
        fields = ['language']

class BooksBookSubjectsSerializer(serializers.ModelSerializer):
    subject = BooksSubjectSerializer()

    class Meta:
        model = BooksBookSubjects
        fields = ['subject']

class BooksBookFormatSerializer(serializers.ModelSerializer):
    mime_type = serializers.CharField()
    url = serializers.CharField()

    class Meta:
        model = BooksFormat
        fields = ['mime_type', 'url']



class BooksBookSerializer(serializers.ModelSerializer):
    authors = BooksBookAuthorsSerializer(source='booksbookauthors_set', many=True)
    bookshelves = BooksBookBookshelvesSerializer(source='booksbookbookshelves_set', many=True)
    languages = BooksBookLanguagesSerializer(source='booksbooklanguages_set', many=True)
    subjects = BooksBookSubjectsSerializer(source='booksbooksubjects_set', many=True)
    formats = BooksBookFormatSerializer(source='booksformat_set', many=True)

    class Meta:
        model = BooksBook
        fields = ['title', 'download_count', 'gutenberg_id', 'media_type', 'authors', 'bookshelves', 'languages', 'subjects', 'formats']