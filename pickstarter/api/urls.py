from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CollectViewSet, PaymentViewSet


router_v1 = DefaultRouter()
router_v1.register(r'^collects', CollectViewSet, basename='api_collects')
router_v1.register(
    r'^collects/(?P<collect_id>\d+)/payments',
    PaymentViewSet,
    basename='api_payments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
