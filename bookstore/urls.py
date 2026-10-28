from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bookstore/v1/", include("product.urls")),
    path("bookstore/v1/", include("order.urls")),
    path("api-token-auth/", obtain_auth_token, name="api-token-auth"),
]

if settings.DEBUG and not settings.TESTING:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
