from django.urls import path
from . import views

urlpatterns = [
    path('reg/', views.user_registration, name='reg'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('order/', views.order, name='order'),
    path('order-list/', views.orderlist, name='order-list'),
    path('update-order/<str:pk>', views.update_order, name='update-order'),
    path('order_details/<str:pk>', views.show_order, name='order_details'),
    path('delete_order/<str:pk>', views.delete_order, name='delete_order'),
    path('category_details/ <str:pk>',
         views.show_category, name='category_details'),

]
