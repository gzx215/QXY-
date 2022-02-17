from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from store.models import Book, UserProfile
from store.serializers import BookSerializers


class CartViewSets(viewsets.ViewSet, mixins.CreateModelMixin):
    permissions = [permissions.IsAuthenticated]

    def list(self, request):
        profile = get_object_or_404(UserProfile.objects.all(), user=request.user)
        return Response(BookSerializers(profile.cart.all(), many=True).data)

    def retrieve(self, request, pk=None):
        profile = get_object_or_404(UserProfile.objects.all(), user=request.user)
        book = get_object_or_404(profile.cart.all(), Id=pk)
        return Response(BookSerializers(book).data)

    def create(self, request, **kwargs):
        profile: UserProfile = get_object_or_404(UserProfile.objects.all(), user=request.user)
        book = get_object_or_404(Book.objects.all(), Id=request.data['Id'])
        profile.cart.add(book)
        return Response({'detail': '添加购物车成功！'})

    def destroy(self, request, pk=None):
        profile: UserProfile = get_object_or_404(UserProfile.objects.all(), user=request.user)
        book = get_object_or_404(profile.cart.all(), Id=pk)
        profile.cart.remove(book)
        return Response({'detail': '删除成功'})
 