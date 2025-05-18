"""
URL configuration for drf_course project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# default
from django.urls import path

# user defined
from django.contrib import admin
from rest_framework import routers
from core import views as core_views
from rest_framework.authtoken.views import obtain_auth_token
# for ecommerce
from ecommerce import views as ecommerce_views


# this router provides auto url routing for api 
#user defined
router = routers.DefaultRouter()
# after ecommerce
router.register(r'item', ecommerce_views.ItemViewSet, basename='item')
router.register(r'order', ecommerce_views.OrderViewSet, basename='order')

urlpatterns = router.urls

urlpatterns += [
    #default
    path("admin/", admin.site.urls),
    #user defined
    path('contact/', core_views.ContactAPIView.as_view()),
    path('api-token-auth/', obtain_auth_token), # gives acess to token auth

]
