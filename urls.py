from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_login, name='login'),
    path('index/',views.index,name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('spentdata/', views.add_spent_data, name='add_spent_data'),
    path('creditdata/', views.add_credit_data, name='add_credit_data'),
 ]