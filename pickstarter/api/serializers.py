from collects.models import Collect, Payment

from rest_framework import serializers


class CollectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collect
        fields = (
            'id', 'author', 'title', 'event', 'description', 'goal_sum',
            'cover', 'end_date',
        )


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('id', 'author', 'payment', 'collect', 'created',)


class CollectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collect
        fields = ('title', 'goal_sum', 'end_date',)
