from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from collects.models import Collect, Payment

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (
    CollectSerializer, CollectListSerializer, PaymentSerializer
)


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return CollectListSerializer
        return CollectSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CollectViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(CollectViewSet, self).perform_destroy(serializer)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        collect_id = self.kwargs.get('collect_id')
        new_queryset = Payment.objects.filter(collect=collect_id)
        return new_queryset

    def perform_create(self, serializer):
        collect_id = self.kwargs.get('collect_id')
        collect = get_object_or_404(Collect, id=collect_id)
        serializer.save(author=self.request.user, collect=collect)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PaymentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(PaymentViewSet, self).perform_destroy(serializer)
