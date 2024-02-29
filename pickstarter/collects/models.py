from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

EVENTS = [
    'День рождения',
    'Свадьба',
    'Свидание',
    'Подарок',
    'Бездомным котикам и пёсикам',
    'Благотворительность',
    'Другое'
]


class Collect(models.Model):
    author = author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collects'
    )
    title = models.CharField(max_length=200)
    event = models.CharField(choices=EVENTS)
    description = models.TextField()
    # цель сбора: если оставить None, то бесконечная
    goal_sum = models.IntegerField(blank=True, null=True, default=None)
    cover = models.ImageField(upload_to='collects/', null=True, blank=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Payment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='payments'
    )
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    collect = models.ForeignKey(
        Collect, on_delete=models.SET_NULL, related_name='payments'
    )
    created = models.DateTimeField(
        'Дата платежа', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return f'{self.payment} руб. на "{self.collect}"'
