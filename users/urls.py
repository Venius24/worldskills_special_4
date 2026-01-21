from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('profile', views.profile, name='profile'),
    path('addresses', views.AddressListCreateView.as_view(), name='addresses'),
    path('addresses/<int:pk>', views.AddressDetailView.as_view(), name='address-detail'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('security-questions', views.security_questions, name='security-questions'),
]