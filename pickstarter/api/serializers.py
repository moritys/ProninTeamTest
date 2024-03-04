import base64

from collects.models import Collect, Payment

from rest_framework import serializers
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.mail import send_mail


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CollectSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    cover = Base64ImageField(required=False, allow_null=True)
    current_sum = serializers.SerializerMethodField()
    people_fees = serializers.SerializerMethodField()

    class Meta:
        model = Collect
        fields = (
            'id', 'author', 'title', 'event', 'description', 'goal_sum',
            'current_sum', 'people_fees', 'cover', 'end_date',
        )

    def create(self, validated_data):
        collect = Collect.objects.create(**validated_data)
        send_mail(
            'Успешное создание сбора',
            'Ваш сбор успешно создан!',
            'pickstarter@gmail.com',
            ['google@google.com'],  # тестовый адрес
            # вернуть этот параметр для прода
            # [self.context['request'].user.email],
            fail_silently=True,
        )

        return collect

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

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        send_mail(
            'Успешное создание платежа',
            'Ваш платеж успешно создан!',
            'pickstarter@gmail.com',
            ['google@google.com'],  # тестовый адрес
            # вернуть этот параметр для прода
            # [self.context['request'].user.email],
            fail_silently=True,
        )

        return payment


class CollectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collect
        fields = ('author', 'title', 'goal_sum', 'end_date',)
