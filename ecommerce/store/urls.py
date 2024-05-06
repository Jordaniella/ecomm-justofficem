from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('store/', views.store, name="store"),
    path('product/<int:id>/', views.see_product, name="product"),
    path('product/search/', views.search_products, name="search"),
    path('product/filter/', views.filter_products, name="filter"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.update_item, name="update_item"),
    path('process_order/', views.process_order, name="process_order")
]
