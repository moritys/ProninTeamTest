from collects.models import Collect, Payment

from rest_framework import serializers
from django.utils import timezone


class CollectSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    current_sum = serializers.SerializerMethodField()
    people_fees = serializers.SerializerMethodField()

    class Meta:
        model = Collect
        fields = (
            'id', 'author', 'title', 'event', 'description', 'goal_sum',
            'current_sum', 'people_fees', 'cover', 'end_date',
        )

    def get_current_sum(self, obj):
        payments = obj.payments.all()
        total = sum(payment.payment for payment in payments)
        return total

    def get_people_fees(self, obj):
        payers = obj.payments.values('author').distinct()
        count = payers.count()
        return count

    def validate_end_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                'Дата окончания не может быть в прошлом.'
            )
        return value


class PaymentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Payment
        fields = ('id', 'author', 'payment', 'created',)


class CollectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collect
        fields = ('author', 'title', 'goal_sum', 'end_date',)
