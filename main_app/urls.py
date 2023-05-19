from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import TransactionUpdateView, TransactionDeleteView


urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('accounts/', views.accounts_index, name='accounts'),
  path('accounts/<int:pk>/', views.account_detail, name='account_detail'),
  path('accounts/create/', views.AccountCreate.as_view(), name='create_account'),
  path('accounts/<int:pk>/update/', views.AccountUpdate.as_view(), name='account_update'),
  path('accounts/<int:pk>/delete/', views.AccountDelete.as_view(), name='account_delete'),
  path('accounts/<int:pk>/add_transaction/', views.add_transaction, name='add_transaction'),
  path('acccounts/<int:transaction_id>/assoc_toy/<int:tag_id>/', views.assoc_tag, name='assoc_toy'),
  path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
  path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('accounts/signup/', views.signup, name='signup'),
  path('transactions/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
]