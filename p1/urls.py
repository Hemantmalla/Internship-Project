"""
URL configuration for p1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from restaurant import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback, name='feedback'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('privacy/', views.privacy, name='privacy'),
    path('profile/', views.profile, name='profile'),
    path('reserve/', views.reserve, name='reserve'),
    path('term/', views.term, name='term'),
    path('login/', views.login_page, name='login'),
    path('waiter_form/', views.waiter_form, name='waiter_form'),
    path('role/', views.role_selection, name='role'),
    path('add-item/', views.add_menu_item, name='add_item'),
    path("add-to-cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("update-qty/<int:item_id>/<str:action>/", views.update_qty, name="update_qty"),
    path("generate-bill/", views.generate_bill, name="generate_bill"),
    path("generated-bill/", views.generated_bill_view, name="generated_bill"),
    path("order-detail/", views.order_list_view, name="orderdetail"),
    path('update_res/<int:res_id>/', views.update_res, name='update_res'),
    path('delete_res/<int:res_id>/', views.delete_res, name='delete_res'),
    path("register-storage/", views.register_storage, name="register_storage"),
]
