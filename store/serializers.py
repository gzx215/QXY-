from rest_framework import serializers
from store.models import Book


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
 