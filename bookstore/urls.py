from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bookstore/v1/", include("product.urls")),
    path("bookstore/v1/", include("order.urls")),
]