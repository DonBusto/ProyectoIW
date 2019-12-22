"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include
import appIndiTDE.views as views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django_filters.views import FilterView
from appIndiTDE.filters import RopaFilter
from appIndiTDE.views import RopaViewSet, FavoritosViewSet
from rest_framework import routers


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('ropas', RopaViewSet)
router.register('favoritos', FavoritosViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name = 'index'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('clothe/<int:id_clothe>', views.clothe, name ='clothe'),
    path('brand/<str:brand_name>', views.brand, name ='brand'),
    path('brand/eng/<str:brand_name>', views.brand_eng, name ='brand_eng'),
    path('shop/', views.category, name ='category'),
    path('favourites/', views.favourites, name='favourites'),
    url('api/', include(router.urls))

]
urlpatterns += i18n_patterns(
    path('contact/', views.contact, name = 'contact'),
    prefix_default_language=False,
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
