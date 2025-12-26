from django.urls import include, path


from .views import (
    profile_view, unauthorized_view,
    CheckRefreshTokenAPIView, CheckRefreshTokenV2APIView,
    UserProfileAPIView,
    CallbackJWTView, OAuthTokenExchangeView,
    LoginView, LoginSPAView, LogoutView, LogoutV2View,
    RegisterWebhookView, UpdateWebhookView,
    LogoutWebhookView, DeleteWebhookView,
    TokenRefreshView, TokenRefreshV2View,
)


webhook = [
    path('user/logout/', LogoutWebhookView.as_view(), name='user-logout'),
    path('user/delete/', DeleteWebhookView.as_view(), name='user-delete'),
    path('user/register/', RegisterWebhookView.as_view(), name='user-register'),
    path('user/update/', UpdateWebhookView.as_view(), name='user-update'),
]

iam_client_urls = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('login/spa/', LoginSPAView.as_view(), name='user-login-spa'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('logout/v2/', LogoutV2View.as_view(), name='user-logout-v2'),
    path('users/me/', UserProfileAPIView.as_view(), name='user-profile'),
    path('token/check/', CheckRefreshTokenAPIView.as_view(), name='token-check'),
    path('token/check/v2/', CheckRefreshTokenV2APIView.as_view(), name='token-check-v2'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/refresh/v2/', TokenRefreshV2View.as_view(), name='token-refresh-v2'),

    # OAuth 回调
    path('callback/', CallbackJWTView.as_view(), name='callback'),
    path('oauth/token/', OAuthTokenExchangeView.as_view(), name='oauth-token'),

    # webhook
    path('webhook/', include((webhook, 'webhook'), namespace="webhook")),

    # 静态页面，可用于剥离前端的调试
    path('home/', profile_view, name='home'),
    path('unauthorized/', unauthorized_view, name='unauthorized'),
]
