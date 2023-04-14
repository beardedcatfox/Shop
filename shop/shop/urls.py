from django.urls import path

from shop import views

urlpatterns = [
    path('', views.book_list, name='home'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('cart-add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/password/', views.CustomPasswordChangeView.as_view(), name='password'),
    path('create-order/', views.order_create, name='create_order'),
    path('orderlist/', views.orderlist, name='order_list'),
    path('logout/', views.logout_view, name='logout'),
]
