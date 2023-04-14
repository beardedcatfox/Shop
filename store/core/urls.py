"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from book.views import AuthorList, BookList, OrderList, create_order

from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework.authtoken import views


urlpatterns = [
    path('api/', include(routers.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('books/', BookList.as_view(), name='book-list'),
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('orders/create/', create_order, name='create-order'),
    path('status/', OrderList.as_view(), name='order-list'),
]
