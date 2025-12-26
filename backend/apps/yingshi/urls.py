from django.urls import path
from . import views

app_name = 'yingshi'

urlpatterns = [
    path('webhook/', views.YingshiWebhookView.as_view(), name='webhook'),
    # 可选：DRF风格的视图
    # path('webhook-drf/', views.yingshi_webhook_drf, name='webhook_drf'),
]
