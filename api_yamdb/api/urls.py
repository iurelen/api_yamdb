from django.urls import include, path

from .v1.routers import auth_urls, router_v1

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls)),
]
