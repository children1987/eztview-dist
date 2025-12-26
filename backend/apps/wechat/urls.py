from django.urls import path
from backend.apps.wechat.views import CallbackView, OpenPlatformBindView,  QrCodeView, \
    WechatJsSdkView

urlpatterns = [
    path('callback/', CallbackView.as_view()),
    path('qrcode/', QrCodeView.as_view()),
    path('jssdk/', WechatJsSdkView.as_view()),
    # 暂未启用
    path('open/bind/', OpenPlatformBindView.as_view()),
]
