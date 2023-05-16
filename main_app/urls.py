from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('accounts/', views.accounts_index, name='accounts'),
  path('accounts/<int:account_id>/', views.accounts_detail, name='detail'),
]