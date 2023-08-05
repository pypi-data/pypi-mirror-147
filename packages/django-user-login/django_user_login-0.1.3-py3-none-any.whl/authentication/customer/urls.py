from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('<str:username>/', views.homepage, name='homepage')
]
