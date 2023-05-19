from django.urls import path
from account import views

urlpatterns = [
    path('user',views.createUser),
    path('user/auth',views.verifyUser),
]