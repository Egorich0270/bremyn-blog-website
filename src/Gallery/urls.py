from django.urls import path
from django.views.i18n import set_language

from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('gallery', permanent=False)),
    path('gallery/', views.gallery_view, name='gallery'),
    path('about/', views.about_view, name='about'),
    path('cooperation/', views.cooperation_view, name='cooperation'),
    path('contact/', views.contact_view, name='contact'),
    path('set-language/', set_language, name='set_language'),
    path('card/<int:pk>/', views.card_detail, name='card_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
